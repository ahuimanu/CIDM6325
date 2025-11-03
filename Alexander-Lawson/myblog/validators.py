import os
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from PIL import Image


@deconstructible
class ImageValidator:
    """
    Custom image validator for security and quality checks
    """
    
    def __init__(self, max_size=5*1024*1024, min_width=100, min_height=100, 
                 max_width=5000, max_height=5000):
        self.max_size = max_size
        self.min_width = min_width
        self.min_height = min_height
        self.max_width = max_width
        self.max_height = max_height
        
        # Allowed file extensions and MIME types
        self.allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        self.allowed_mimetypes = [
            'image/jpeg', 'image/png', 'image/gif', 'image/webp'
        ]
    
    def __call__(self, image):
        # File size check
        if image.size > self.max_size:
            raise ValidationError(
                f'Image file size ({image.size/1024/1024:.1f}MB) exceeds maximum allowed size '
                f'({self.max_size/1024/1024:.1f}MB).'
            )
        
        # File extension check
        ext = os.path.splitext(image.name)[1].lower()
        if ext not in self.allowed_extensions:
            raise ValidationError(
                f'Invalid file extension "{ext}". Allowed extensions: '
                f'{", ".join(self.allowed_extensions)}'
            )
        
        # Content type check
        if hasattr(image, 'content_type'):
            if image.content_type not in self.allowed_mimetypes:
                raise ValidationError(
                    f'Invalid file type "{image.content_type}". '
                    f'Please upload a valid image file.'
                )
        
        # Image dimension validation using Pillow
        try:
            with Image.open(image) as img:
                width, height = img.size
                
                # Check minimum dimensions
                if width < self.min_width or height < self.min_height:
                    raise ValidationError(
                        f'Image dimensions ({width}x{height}) are too small. '
                        f'Minimum size: {self.min_width}x{self.min_height} pixels.'
                    )
                
                # Check maximum dimensions
                if width > self.max_width or height > self.max_height:
                    raise ValidationError(
                        f'Image dimensions ({width}x{height}) are too large. '
                        f'Maximum size: {self.max_width}x{self.max_height} pixels.'
                    )
                
                # Verify image integrity
                img.verify()
                
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(
                'Invalid or corrupted image file. Please upload a valid image.'
            )
    
    def __eq__(self, other):
        return (
            isinstance(other, ImageValidator) and
            self.max_size == other.max_size and
            self.min_width == other.min_width and
            self.min_height == other.min_height and
            self.max_width == other.max_width and
            self.max_height == other.max_height
        )


def validate_image_content(image):
    """
    Additional security validation for image content
    """
    # Check for malicious file headers
    image.seek(0)
    header = image.read(1024)
    image.seek(0)
    
    # Check for script tags or suspicious content in first 1KB
    suspicious_patterns = [
        b'<script', b'javascript:', b'vbscript:', 
        b'onload=', b'onerror=', b'<?php'
    ]
    
    header_lower = header.lower()
    for pattern in suspicious_patterns:
        if pattern in header_lower:
            raise ValidationError(
                'Potentially malicious content detected in image file.'
            )
    
    return image