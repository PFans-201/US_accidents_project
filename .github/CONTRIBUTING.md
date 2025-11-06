# Contributing to US Accidents Road Quality Analysis

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)

## Code of Conduct

This project adheres to a code of professional conduct. By participating, you are expected to uphold this standard. Please report unacceptable behavior to the project maintainers.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/us-accidents-road-quality.git
   cd us-accidents-road-quality
   ```
3. **Set up development environment**:
   ```bash
   make install-dev
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/03-your-feature-name
   ```

## Development Workflow

### Branch Naming Convention
- `feature/[step-number]-[description]` - New features
  - Example: `feature/03-spatial-join-implementation`
- `bugfix/[issue-number]-[description]` - Bug fixes
  - Example: `bugfix/12-fix-missing-coordinates`
- `docs/[description]` - Documentation updates
  - Example: `docs/update-methodology`
- `paper/[section]` - Research paper sections
  - Example: `paper/results-discussion`

### Step-Based Development
Our project follows a 9-step implementation plan. When working on a specific step:

1. Create a branch: `feature/[step-number]-[description]`
2. Implement the step according to `docs/PROJECT_SPECIFICATION.md`
3. Add/update tests
4. Update documentation
5. Submit pull request referencing the step number

## Coding Standards

### Python Style Guide
- Follow **PEP 8** guidelines
- Use **type hints** for all function signatures
- Maximum line length: **88 characters** (Black default)
- Use **docstrings** for all public functions and classes

### Docstring Format
```python
def spatial_join_accidents_roads(
    accidents_gdf: gpd.GeoDataFrame,
    roads_gdf: gpd.GeoDataFrame,
    max_distance: float = 100.0
) -> gpd.GeoDataFrame:
    """
    Perform spatial join between accident points and road segments.
    
    Args:
        accidents_gdf: GeoDataFrame containing accident points
        roads_gdf: GeoDataFrame containing road network segments
        max_distance: Maximum distance in meters for matching (default: 100.0)
    
    Returns:
        GeoDataFrame with accidents joined to nearest road segments
    
    Raises:
        ValueError: If input GeoDataFrames have mismatched CRS
        
    Example:
        >>> accidents = load_accidents_data()
        >>> roads = load_osm_roads()
        >>> joined = spatial_join_accidents_roads(accidents, roads)
    """
```

### Code Quality Tools
Run before committing:
```bash
make format    # Auto-format with Black
make lint      # Check with flake8 and pylint
make type-check # Type check with mypy
make test      # Run test suite
```

## Commit Messages

### Format
```
[STEP-X] Brief description (50 chars or less)

More detailed explanatory text if necessary. Wrap at 72 characters.
Explain the problem that this commit is solving and why this approach.

- Bullet points are okay
- Use present tense: "Add feature" not "Added feature"
- Reference issues and pull requests

Closes #123
```

### Examples
```
[STEP-1] Add accidents data loader with geometry conversion

Implements load_accidents_data() function that reads US Accidents CSV,
creates Point geometries from lat/lon coordinates, and returns a
GeoDataFrame with WGS84 projection.

- Handles missing coordinates with logging
- Validates data types
- Adds unit tests

Related to #15
```

```
[STEP-3] Implement spatial join with distance threshold

Adds spatial_join_accidents_roads() function with configurable max
distance parameter. Uses rtree spatial indexing for performance.

Closes #23
```

## Pull Request Process

### Before Submitting
1. ✅ Update relevant documentation
2. ✅ Add/update tests (maintain >80% coverage)
3. ✅ Run `make test` - all tests pass
4. ✅ Run `make lint` - no linting errors
5. ✅ Run `make format` - code formatted
6. ✅ Update `CHANGELOG.md` if applicable

### PR Template
```markdown
## Description
Brief description of changes

## Step Reference
- [ ] Step 1: Data Loading and Preparation
- [ ] Step 2: OpenStreetMap Data Acquisition
- [x] Step 3: Spatial Join Operation
(check applicable steps)

## Type of Change
- [ ] Bug fix
- [x] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
Describe testing performed:
- Unit tests added for spatial_join module
- Validated with sample dataset (1000 accidents)
- Performance: processes 10k records in 2.3 seconds

## Checklist
- [x] Code follows project style guidelines
- [x] Self-review completed
- [x] Comments added for complex logic
- [x] Documentation updated
- [x] Tests added and passing
- [x] No new warnings generated

## Screenshots/Outputs
(if applicable - e.g., plots, maps, results)
```

### Review Process
- PRs require **at least 1 approval** from a team member
- All CI checks must pass
- Address all review comments
- Keep PRs focused - one feature/fix per PR

## Testing

### Writing Tests
- Place tests in `tests/` directory
- Name test files: `test_[module_name].py`
- Use descriptive test function names: `test_spatial_join_with_missing_coordinates()`

### Test Structure
```python
import pytest
from src.data.spatial_join import spatial_join_accidents_roads

def test_spatial_join_basic():
    """Test spatial join with simple input."""
    # Arrange
    accidents_gdf = create_sample_accidents()
    roads_gdf = create_sample_roads()
    
    # Act
    result = spatial_join_accidents_roads(accidents_gdf, roads_gdf)
    
    # Assert
    assert len(result) == len(accidents_gdf)
    assert "surface" in result.columns

def test_spatial_join_handles_missing_coords():
    """Test that function handles accidents with missing coordinates."""
    # Test implementation
```

### Running Tests
```bash
make test           # Run all tests
make test-cov       # Run with coverage report
pytest tests/test_spatial_join.py -v  # Run specific test file
pytest tests/test_spatial_join.py::test_spatial_join_basic  # Run specific test
```

## Documentation

### Code Documentation
- Add docstrings to all public functions, classes, and modules
- Update `docs/` markdown files when changing architecture or methodology
- Include code examples in docstrings

### Research Paper
- Paper sections are in `paper/sections/`
- Use LaTeX for all paper content
- Reference code and results from notebooks
- Update `references.bib` for citations

## Questions?

If you have questions or need clarification:
1. Check existing issues and discussions
2. Review `docs/PROJECT_SPECIFICATION.md`
3. Reach out to team members via agreed communication channel
4. Create a new issue with the `question` label

## Recognition

Contributors will be acknowledged in:
- `README.md` Contributors section
- Research paper acknowledgments
- `paper/appendices/B_contribution_hours.tex`

Thank you for contributing! 🎉
