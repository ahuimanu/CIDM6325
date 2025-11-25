# Licensing and Compliance: Airport Data

This document details the licensing terms, compliance obligations, and risk management for airport data used in TravelMathLite.

## Executive Summary

- **Dataset**: OurAirports (https://ourairports.com/data/)
- **License**: Public Domain
- **Attribution**: Optional but appreciated
- **Risk Level**: Low
- **Compliance Status**: ✅ Compliant

## Dataset Information

### OurAirports

**Source**: https://ourairports.com/data/  
**Repository**: https://github.com/davidmegginson/ourairports-data  
**Primary Files Used**:
- `airports.csv` - Airport location and metadata
- `countries.csv` - Country code mappings (optional reference)
- `regions.csv` - Regional subdivision mappings (optional reference)

**Update Frequency**: Nightly  
**Data Coverage**: Global (70,000+ airports)

## Licensing Terms

### Public Domain Dedication

OurAirports explicitly releases all data to the **Public Domain** with no restrictions on use.

**Official Statement** (from https://ourairports.com/data/):

> "All data is released to the Public Domain, and comes with no guarantee of accuracy or fitness for use."

### What This Means

✅ **Permitted Uses**:
- Commercial use without restriction
- Modification and derivative works
- Redistribution in any format
- Private/internal use
- Educational and research purposes
- Creating competing services

❌ **No Restrictions**:
- No attribution required
- No share-alike obligations
- No trademark restrictions on data content
- No registration or API keys needed

⚠️ **No Warranties**:
- No guarantee of accuracy
- No guarantee of fitness for purpose
- No liability for errors or omissions

## Attribution Practice

### TravelMathLite Approach

While attribution is **not required**, TravelMathLite provides attribution as a best practice:

**Attribution Text** (used in documentation and admin interface):

> "Airport data sourced from OurAirports (https://ourairports.com/data/), released to the Public Domain."

**Attribution Locations**:
1. **Documentation**: This file and ADR-1.0.1
2. **README**: Project README mentions data source
3. **Admin Interface**: Footer or data source page (optional, not yet implemented)
4. **API Responses**: Optional `data_source` metadata field (not yet implemented)
5. **About Page**: Optional attribution page (not yet implemented)

### Why Provide Attribution

1. **Community Standards**: Respects open data norms
2. **Transparency**: Users know data provenance
3. **Credit**: Acknowledges OurAirports' volunteer efforts
4. **Updates**: Makes it easier to track data source changes
5. **Trust**: Builds confidence in data quality

## Compliance Obligations

### Legal Requirements

**None**. Public Domain dedication removes all legal obligations.

### Best Practices

Despite no legal requirements, TravelMathLite follows these practices:

1. **Attribution**: Provide credit as described above
2. **No Misrepresentation**: Don't claim ownership of OurAirports data
3. **Accuracy Disclaimers**: Acknowledge data limitations
4. **Update Documentation**: Maintain accurate source references
5. **License Tracking**: Document license status in ADR and code

## Risk Assessment

### License Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| License change | Very Low | Low | Public Domain is irrevocable for released data |
| Attribution dispute | Very Low | Very Low | Attribution provided despite not required |
| Data accuracy issues | Medium | Medium | Validation checks, dry-run testing, error handling |
| Service discontinuation | Low | Medium | Data cached locally, periodic updates only |
| Trademark issues | Very Low | Very Low | OurAirports branding not used in app name |

**Overall Risk Level**: **Low** ✅

### Data Quality Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Incomplete IATA codes | High | Low | Filter to IATA-only airports, validation checks |
| Coordinate errors | Low | Medium | Range validation (-90 to 90, -180 to 180) |
| Stale data | Medium | Low | Weekly automated updates |
| Missing airports | Low | Low | Community-driven updates upstream |
| Inconsistent naming | Medium | Low | Accept as-is, admin tools for local corrections |

**Overall Risk Level**: **Low** ✅

### Operational Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Download failures | Low | Low | Error handling, retry logic, local cache |
| Large file size | Low | Very Low | Row-by-row processing, minimal memory footprint |
| Rate limiting | Very Low | Very Low | No API keys, direct CSV downloads |
| SSL/TLS errors | Low | Low | SSL context handling in download code |
| Encoding issues | Low | Low | UTF-8 handling, validation |

**Overall Risk Level**: **Very Low** ✅

## Warranty and Liability

### OurAirports Disclaimer

OurAirports provides data "as-is" with:
- ❌ No warranty of accuracy
- ❌ No warranty of fitness for use
- ❌ No warranty of completeness
- ❌ No liability for damages

### TravelMathLite Responsibilities

As the data consumer, TravelMathLite:
1. **Validates Data**: Implements validation checks before use
2. **Tests Thoroughly**: Uses dry-run mode and comprehensive tests
3. **Handles Errors**: Gracefully handles invalid or missing data
4. **Documents Limitations**: Informs users of data source and limitations
5. **Accepts Risk**: Takes responsibility for fitness-for-purpose

### User-Facing Disclaimers

Consider adding disclaimers in:
- Terms of Service (if applicable)
- About/Data Source page
- API documentation (if applicable)
- Error messages for data-related failures

**Example Disclaimer**:
> "Airport location data is sourced from publicly available datasets and may contain inaccuracies. TravelMathLite provides this information for convenience only and makes no guarantees about accuracy or completeness."

## Compliance Checklist

### Initial Compliance (Completed)

- [x] ✅ Verify OurAirports license is Public Domain
- [x] ✅ Document license terms in this file
- [x] ✅ Document license terms in ADR-1.0.1
- [x] ✅ Add attribution text to documentation
- [x] ✅ Implement data validation (validate_airports command)
- [x] ✅ Add error handling for data quality issues
- [x] ✅ Test with dry-run mode before production use
- [x] ✅ Review and accept "no warranty" implications

### Ongoing Compliance (Recommended)

- [ ] Add attribution to user-facing pages (About page)
- [ ] Consider data source metadata in API responses
- [ ] Add disclaimer to Terms of Service (if created)
- [ ] Monitor OurAirports for any license changes (unlikely)
- [ ] Document any local data corrections made
- [ ] Review compliance annually or on major updates

## Alternative Data Sources (Not Used)

For reference, these alternatives were considered but not selected:

### OpenFlights
- **License**: ODbL (Open Database License)
- **Requirements**: Attribution + Share-Alike
- **Reason Not Selected**: More restrictive than OurAirports

### Commercial APIs (e.g., Amadeus, Skyscanner)
- **License**: Proprietary, Terms of Service
- **Requirements**: API keys, rate limits, attribution, commercial terms
- **Reason Not Selected**: Cost, complexity, legal obligations

### Government Sources (e.g., FAA, ICAO)
- **License**: Varies by country (US government data is Public Domain)
- **Requirements**: Varies
- **Reason Not Selected**: Less comprehensive global coverage

## Updates and Changes

### License Monitoring

**Frequency**: Annual review (or when notified of changes)  
**Responsible**: Project maintainer  
**Process**:
1. Visit https://ourairports.com/data/
2. Review "Terms of use" section
3. Check GitHub repository for LICENSE file changes
4. Update documentation if terms change
5. Assess impact on TravelMathLite usage

**Change History**:
- 2025-11-14: Initial compliance review - Public Domain confirmed
- (Future changes documented here)

### Data Source Migration

If OurAirports becomes unavailable or changes terms:

**Backup Options**:
1. Fork davidmegginson/ourairports-data repository (already Public Domain)
2. Switch to OpenFlights (requires attribution + share-alike)
3. Use FAA data for US airports + international alternatives
4. Commercial API with appropriate license

**Migration Checklist**:
- [ ] Evaluate alternative licensing terms
- [ ] Update ADR-1.0.1 with new data source decision
- [ ] Modify import_airports command for new format
- [ ] Update validation rules if needed
- [ ] Test with new data source
- [ ] Update all attribution text
- [ ] Document migration in CHANGELOG

## References

### Primary Sources

- **OurAirports Data Page**: https://ourairports.com/data/
- **OurAirports About**: https://ourairports.com/about.html
- **OurAirports GitHub**: https://github.com/davidmegginson/ourairports-data
- **Public Domain Definition**: https://creativecommons.org/publicdomain/

### Project Documentation

- **ADR-1.0.1**: Dataset source for airports and cities
- **Update Automation**: docs/travelmathlite/update-automation-airports.md
- **Schema Mapping**: docs/travelmathlite/schema-mapping-airports.md
- **Brief 06**: docs/travelmathlite/briefs/adr-1.0.1/brief-ADR-1.0.1-06-licensing-compliance.md

### Legal Resources

- **Public Domain Explained**: https://fairuse.stanford.edu/overview/public-domain/welcome/
- **Open Data Commons**: https://opendatacommons.org/
- **Creative Commons Public Domain**: https://creativecommons.org/publicdomain/

## Contact

For questions about OurAirports licensing:
- **Website**: https://ourairports.com/contact.html
- **GitHub Issues**: https://github.com/davidmegginson/ourairports-data/issues

For questions about TravelMathLite compliance:
- **Issue Tracker**: https://github.com/ahuimanu/CIDM6325/issues
- **Project Maintainer**: See repository CODEOWNERS

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-14  
**Status**: ✅ Compliant  
**Next Review**: 2026-11-14 (or on major updates)
