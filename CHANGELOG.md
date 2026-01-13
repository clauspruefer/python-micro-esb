# Changelog

## Version 1.1

- Add user-based service call routing via ServiceRouter class
- Introduce `property_dict` functionality for flexible property access excluding internal system properties
- Support recursive class hierarchy object deserialization in ServiceExecuter
- Improve JSONTransformer robustness with `_SYSClassNames` tracking for hierarchy processing
- Add property registration feature for internal system properties via `register_property()`
- Modify Example 02 to use NoSQL MongoDB backend for certificate management
- Add Example 04 with NLAP proxy integration documentation
- Add comprehensive unit and integration tests for recursive json_transform()
- Cleanup recursive hierarchy processing code in `execute_get_hierarchy()`
- Update documentation for version 1.1 features

## Version 1.0

- Working pylint checks
- Adapt documentation

## Version 1.0rc2

- Add CHANGELOG.md
- Correct package metadata (1.0rc2)
- Add dynamic config file inclusion
- Add setting PYTHONPATH via env var
- Add config option to disable logging to stderr

## Version 1.0rc1

- Add correct abc.ABCMeta processing 
