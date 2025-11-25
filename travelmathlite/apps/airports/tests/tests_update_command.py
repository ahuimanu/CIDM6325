"""Tests for update_airports management command."""

from io import StringIO
from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.test import TestCase

from apps.airports.models import Airport


class UpdateAirportsCommandTests(TestCase):
    """Test the update_airports management command."""

    def setUp(self):
        """Set up test fixtures."""
        # Create some initial airports
        Airport.objects.create(
            ident="TEST1",
            name="Test Airport 1",
            airport_type="small_airport",
            latitude_deg=40.0,
            longitude_deg=-105.0,
            iso_country="US",
        )
        Airport.objects.create(
            ident="TEST2",
            name="Test Airport 2",
            airport_type="small_airport",
            latitude_deg=41.0,
            longitude_deg=-106.0,
            iso_country="US",
        )

    @patch("apps.airports.management.commands.update_airports.call_command")
    def test_update_calls_import_command(self, mock_call_command: MagicMock) -> None:
        """Test that update command calls import_airports."""
        out = StringIO()
        call_command("update_airports", "--dry-run", stdout=out)

        # Verify import_airports was called
        mock_call_command.assert_called_once()
        args, _ = mock_call_command.call_args
        self.assertEqual(args[0], "import_airports")

    @patch("apps.airports.management.commands.update_airports.call_command")
    def test_update_dry_run_mode(self, mock_call_command: MagicMock) -> None:
        """Test update command in dry-run mode."""
        out = StringIO()
        call_command("update_airports", "--dry-run", stdout=out)
        output = out.getvalue()

        self.assertIn("DRY RUN MODE", output)
        self.assertIn("No changes will be saved", output)

    @patch("apps.airports.management.commands.update_airports.call_command")
    def test_update_shows_initial_count(self, mock_call_command: MagicMock) -> None:
        """Test that update command shows initial airport count."""
        out = StringIO()
        call_command("update_airports", "--dry-run", stdout=out)
        output = out.getvalue()

        self.assertIn("Current airports in database: 2", output)

    @patch("apps.airports.management.commands.update_airports.call_command")
    def test_update_with_filter_iata(self, mock_call_command: MagicMock) -> None:
        """Test update command with IATA filter."""
        out = StringIO()
        call_command("update_airports", "--filter-iata", "--dry-run", stdout=out)

        # Verify filter_iata was passed to import command
        _, kwargs = mock_call_command.call_args
        self.assertTrue(kwargs.get("filter_iata"))

    @patch("apps.airports.management.commands.update_airports.call_command")
    def test_update_with_custom_url(self, mock_call_command: MagicMock) -> None:
        """Test update command with custom URL."""
        custom_url = "https://example.com/airports.csv"
        out = StringIO()
        call_command("update_airports", f"--url={custom_url}", "--dry-run", stdout=out)

        # Verify URL was passed to import command
        _, kwargs = mock_call_command.call_args
        self.assertEqual(kwargs.get("url"), custom_url)

    @patch("apps.airports.management.commands.update_airports.call_command")
    def test_update_shows_summary(self, mock_call_command: MagicMock) -> None:
        """Test that update command shows summary information."""
        out = StringIO()
        call_command("update_airports", "--dry-run", stdout=out)
        output = out.getvalue()

        self.assertIn("Airport Data Update", output)
        self.assertIn("Started:", output)
        self.assertIn("Completed:", output)
        self.assertIn("Duration:", output)

    @patch("apps.airports.management.commands.update_airports.call_command")
    def test_update_handles_exceptions(self, mock_call_command: MagicMock) -> None:
        """Test that update command handles exceptions gracefully."""
        # Make import_airports raise an exception
        mock_call_command.side_effect = Exception("Test error")

        out = StringIO()
        call_command("update_airports", "--dry-run", stdout=out)
        output = out.getvalue()

        self.assertIn("Update failed:", output)
        self.assertIn("Test error", output)

    @patch("apps.airports.management.commands.update_airports.call_command")
    def test_update_shows_duration(self, mock_call_command: MagicMock) -> None:
        """Test that update command shows execution duration."""
        out = StringIO()
        call_command("update_airports", "--dry-run", stdout=out)
        output = out.getvalue()

        self.assertIn("Duration:", output)
        self.assertIn("seconds", output)

    @patch("apps.airports.management.commands.update_airports.call_command")
    def test_update_stdout_stderr_passed_to_import(self, mock_call_command: MagicMock) -> None:
        """Test that stdout and stderr are passed to import command."""
        out = StringIO()
        err = StringIO()
        call_command("update_airports", "--dry-run", stdout=out, stderr=err)

        # Verify stdout and stderr were passed
        _, kwargs = mock_call_command.call_args
        self.assertIn("stdout", kwargs)
        self.assertIn("stderr", kwargs)

    def test_update_command_integration(self) -> None:
        """Test update command integration without mocking."""
        # This test actually runs the full update process
        # Note: It will attempt to download data, so it might be slow
        out = StringIO()

        # Use dry-run to avoid actually changing data
        initial_count = Airport.objects.count()

        try:
            call_command("update_airports", "--dry-run", stdout=out)
            output = out.getvalue()

            # Verify output structure
            self.assertIn("Airport Data Update", output)
            self.assertIn(f"Current airports in database: {initial_count}", output)
            self.assertIn("DRY RUN", output)
            self.assertIn("Completed:", output)

            # Verify data wasn't changed (dry run)
            self.assertEqual(Airport.objects.count(), initial_count)

        except Exception as e:
            # Network errors are acceptable in tests
            if "Failed to download" not in str(e):
                raise
