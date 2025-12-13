# backend/algorithms/tests/test_registry.py
"""
Comprehensive tests for AlgorithmRegistry.

Coverage Target: 95%

Test Categories:
1. Registry initialization and state
2. Valid algorithm registration
3. Invalid registration (wrong type, duplicates)
4. Algorithm retrieval (get, errors)
5. Listing algorithms and metadata
6. Metadata exposure (tracer_class not exposed)
7. Helper methods (__contains__, __len__, convenience functions)
"""

import pytest
from algorithms.registry import (
    AlgorithmRegistry,
    registry,
    get_algorithm_names,
    get_algorithm
)
from algorithms.base_tracer import AlgorithmTracer
from typing import List, Dict, Any


# =============================================================================
# Test Group 1: Registry Initialization
# =============================================================================

@pytest.mark.unit
class TestRegistryInitialization:
    """Test registry creation and initial state."""
    
    def test_create_empty_registry(self):
        """New registry starts empty."""
        reg = AlgorithmRegistry()
        assert len(reg) == 0
        assert reg.count() == 0
    
    def test_global_registry_exists(self):
        """Global registry instance is available."""
        assert registry is not None
        assert isinstance(registry, AlgorithmRegistry)
    
    def test_global_registry_has_algorithms(self):
        """Global registry is pre-populated with algorithms."""
        # After register_algorithms() runs on import
        assert len(registry) > 0
        assert 'binary-search' in registry
        assert 'interval-coverage' in registry
    
    def test_empty_registry_list_algorithms(self):
        """Empty registry returns empty list."""
        reg = AlgorithmRegistry()
        assert reg.list_algorithms() == []


# =============================================================================
# Test Group 2: Valid Algorithm Registration
# =============================================================================

@pytest.mark.unit
class TestValidRegistration:
    """Test successful algorithm registration."""
    
    def test_register_minimal_algorithm(self, clean_registry, minimal_tracer):
        """Register algorithm with minimal required fields."""
        clean_registry.register(
            name='test-algo',
            tracer_class=minimal_tracer.__class__,
            display_name='Test Algorithm',
            description='A test algorithm',
            example_inputs=[{'test': 'input'}]
        )
        
        assert clean_registry.count() == 1
        assert 'test-algo' in clean_registry
    
    def test_register_with_input_schema(self, clean_registry, minimal_tracer):
        """Register algorithm with optional input schema."""
        schema = {
            'type': 'object',
            'required': ['value'],
            'properties': {'value': {'type': 'integer'}}
        }
        
        clean_registry.register(
            name='schema-algo',
            tracer_class=minimal_tracer.__class__,
            display_name='Schema Algorithm',
            description='Has input schema',
            example_inputs=[{'value': 42}],
            input_schema=schema
        )
        
        metadata = clean_registry.get_metadata('schema-algo')
        assert metadata['input_schema'] == schema
    
    def test_register_multiple_algorithms(self, clean_registry, minimal_tracer, viz_enrichment_tracer):
        """Register multiple different algorithms."""
        clean_registry.register(
            name='algo-1',
            tracer_class=minimal_tracer.__class__,
            display_name='Algorithm 1',
            description='First algorithm',
            example_inputs=[{}]
        )
        
        clean_registry.register(
            name='algo-2',
            tracer_class=viz_enrichment_tracer.__class__,
            display_name='Algorithm 2',
            description='Second algorithm',
            example_inputs=[{}]
        )
        
        assert clean_registry.count() == 2
        assert 'algo-1' in clean_registry
        assert 'algo-2' in clean_registry
    
    def test_registered_metadata_stored_correctly(self, clean_registry, minimal_tracer):
        """All registration metadata is stored."""
        example_inputs = [
            {'name': 'Example 1', 'input': {'value': 1}},
            {'name': 'Example 2', 'input': {'value': 2}}
        ]
        
        clean_registry.register(
            name='metadata-test',
            tracer_class=minimal_tracer.__class__,
            display_name='Metadata Test',
            description='Testing metadata storage',
            example_inputs=example_inputs,
            input_schema={'type': 'object'}
        )
        
        metadata = clean_registry.get_metadata('metadata-test')
        assert metadata['name'] == 'metadata-test'
        assert metadata['display_name'] == 'Metadata Test'
        assert metadata['description'] == 'Testing metadata storage'
        assert metadata['example_inputs'] == example_inputs
        assert metadata['input_schema'] == {'type': 'object'}


# =============================================================================
# Test Group 3: Invalid Registration
# =============================================================================

@pytest.mark.unit
class TestInvalidRegistration:
    """Test registration error handling."""
    
    def test_register_non_class_raises_error(self, clean_registry):
        """Registering a non-class raises ValueError."""
        with pytest.raises(ValueError, match="tracer_class must be a class"):
            clean_registry.register(
                name='invalid',
                tracer_class="not a class",  # String instead of class
                display_name='Invalid',
                description='Should fail',
                example_inputs=[{}]
            )
    
    def test_register_instance_raises_error(self, clean_registry, minimal_tracer):
        """Registering an instance instead of class raises ValueError."""
        with pytest.raises(ValueError, match="tracer_class must be a class"):
            clean_registry.register(
                name='invalid',
                tracer_class=minimal_tracer,  # Instance, not class
                display_name='Invalid',
                description='Should fail',
                example_inputs=[{}]
            )
    
    def test_register_non_tracer_class_raises_error(self, clean_registry):
        """Registering class not inheriting from AlgorithmTracer raises ValueError."""
        class NotATracer:
            pass
        
        with pytest.raises(ValueError, match="must inherit from AlgorithmTracer"):
            clean_registry.register(
                name='invalid',
                tracer_class=NotATracer,
                display_name='Invalid',
                description='Should fail',
                example_inputs=[{}]
            )
    
    def test_register_duplicate_name_raises_error(self, clean_registry, minimal_tracer):
        """Registering same name twice raises ValueError."""
        # First registration succeeds
        clean_registry.register(
            name='duplicate-test',
            tracer_class=minimal_tracer.__class__,
            display_name='First',
            description='First registration',
            example_inputs=[{}]
        )
        
        # Second registration with same name fails
        with pytest.raises(ValueError, match="already registered"):
            clean_registry.register(
                name='duplicate-test',
                tracer_class=minimal_tracer.__class__,
                display_name='Second',
                description='Should fail',
                example_inputs=[{}]
            )
    
    def test_duplicate_error_message_helpful(self, clean_registry, minimal_tracer):
        """Duplicate registration error message includes algorithm name."""
        clean_registry.register(
            name='my-algo',
            tracer_class=minimal_tracer.__class__,
            display_name='My Algo',
            description='Test',
            example_inputs=[{}]
        )
        
        with pytest.raises(ValueError, match="'my-algo'"):
            clean_registry.register(
                name='my-algo',
                tracer_class=minimal_tracer.__class__,
                display_name='Duplicate',
                description='Test',
                example_inputs=[{}]
            )


# =============================================================================
# Test Group 4: Algorithm Retrieval
# =============================================================================

@pytest.mark.unit
class TestAlgorithmRetrieval:
    """Test retrieving registered algorithms."""
    
    def test_get_registered_algorithm(self, clean_registry, minimal_tracer):
        """Retrieve a registered algorithm's tracer class."""
        clean_registry.register(
            name='get-test',
            tracer_class=minimal_tracer.__class__,
            display_name='Get Test',
            description='Test retrieval',
            example_inputs=[{}]
        )
        
        tracer_class = clean_registry.get('get-test')
        assert tracer_class == minimal_tracer.__class__
        assert issubclass(tracer_class, AlgorithmTracer)
    
    def test_get_can_instantiate_tracer(self, clean_registry, minimal_tracer):
        """Retrieved tracer class can be instantiated."""
        clean_registry.register(
            name='instantiate-test',
            tracer_class=minimal_tracer.__class__,
            display_name='Instantiate Test',
            description='Test instantiation',
            example_inputs=[{}]
        )
        
        tracer_class = clean_registry.get('instantiate-test')
        instance = tracer_class()
        assert isinstance(instance, AlgorithmTracer)
    
    def test_get_unknown_algorithm_raises_keyerror(self, clean_registry):
        """Getting unknown algorithm raises KeyError with helpful message."""
        with pytest.raises(KeyError, match="not found"):
            clean_registry.get('unknown-algorithm')
    
    def test_get_unknown_shows_available_algorithms(self, clean_registry, minimal_tracer):
        """KeyError for unknown algorithm lists available algorithms."""
        clean_registry.register(
            name='available-1',
            tracer_class=minimal_tracer.__class__,
            display_name='Available 1',
            description='Test',
            example_inputs=[{}]
        )
        
        clean_registry.register(
            name='available-2',
            tracer_class=minimal_tracer.__class__,
            display_name='Available 2',
            description='Test',
            example_inputs=[{}]
        )
        
        with pytest.raises(KeyError, match="Available algorithms"):
            clean_registry.get('not-available')


# =============================================================================
# Test Group 5: Metadata Retrieval
# =============================================================================

@pytest.mark.unit
class TestMetadataRetrieval:
    """Test metadata retrieval and exposure."""
    
    def test_get_metadata_returns_all_fields(self, clean_registry, minimal_tracer):
        """get_metadata returns all metadata fields."""
        clean_registry.register(
            name='meta-test',
            tracer_class=minimal_tracer.__class__,
            display_name='Metadata Test',
            description='Full metadata',
            example_inputs=[{'test': 'data'}],
            input_schema={'type': 'object'}
        )
        
        metadata = clean_registry.get_metadata('meta-test')
        
        assert 'name' in metadata
        assert 'display_name' in metadata
        assert 'description' in metadata
        assert 'example_inputs' in metadata
        assert 'input_schema' in metadata
    
    def test_get_metadata_excludes_tracer_class(self, clean_registry, minimal_tracer):
        """get_metadata does NOT include tracer_class (not JSON-serializable)."""
        clean_registry.register(
            name='no-class-test',
            tracer_class=minimal_tracer.__class__,
            display_name='No Class Test',
            description='Should not expose class',
            example_inputs=[{}]
        )
        
        metadata = clean_registry.get_metadata('no-class-test')
        assert 'tracer_class' not in metadata
    
    def test_get_metadata_unknown_raises_keyerror(self, clean_registry):
        """Getting metadata for unknown algorithm raises KeyError."""
        with pytest.raises(KeyError, match="not found"):
            clean_registry.get_metadata('unknown')
    
    def test_metadata_is_copy_not_reference(self, clean_registry, minimal_tracer):
        """get_metadata returns a copy, not the internal reference."""
        clean_registry.register(
            name='copy-test',
            tracer_class=minimal_tracer.__class__,
            display_name='Copy Test',
            description='Original description',
            example_inputs=[{}]
        )
        
        metadata = clean_registry.get_metadata('copy-test')
        metadata['description'] = 'Modified description'
        
        # Get fresh metadata - should be unchanged
        fresh_metadata = clean_registry.get_metadata('copy-test')
        assert fresh_metadata['description'] == 'Original description'


# =============================================================================
# Test Group 6: List All Algorithms
# =============================================================================

@pytest.mark.unit
class TestListAlgorithms:
    """Test listing all registered algorithms."""
    
    def test_list_algorithms_returns_list(self, clean_registry):
        """list_algorithms returns a list."""
        result = clean_registry.list_algorithms()
        assert isinstance(result, list)
    
    def test_list_algorithms_includes_all_registered(self, clean_registry, minimal_tracer):
        """list_algorithms includes all registered algorithms."""
        names = ['algo-a', 'algo-b', 'algo-c']
        
        for name in names:
            clean_registry.register(
                name=name,
                tracer_class=minimal_tracer.__class__,
                display_name=f'Algorithm {name}',
                description=f'Description for {name}',
                example_inputs=[{}]
            )
        
        algorithms = clean_registry.list_algorithms()
        assert len(algorithms) == 3
        
        returned_names = [algo['name'] for algo in algorithms]
        assert set(returned_names) == set(names)
    
    def test_list_algorithms_excludes_tracer_class(self, clean_registry, minimal_tracer):
        """list_algorithms does not include tracer_class in any entry."""
        clean_registry.register(
            name='list-test',
            tracer_class=minimal_tracer.__class__,
            display_name='List Test',
            description='Should not expose class',
            example_inputs=[{}]
        )
        
        algorithms = clean_registry.list_algorithms()
        
        for algo in algorithms:
            assert 'tracer_class' not in algo
    
    def test_list_algorithms_json_serializable(self, clean_registry, minimal_tracer):
        """list_algorithms output is JSON-serializable."""
        import json
        
        clean_registry.register(
            name='json-test',
            tracer_class=minimal_tracer.__class__,
            display_name='JSON Test',
            description='Must be JSON-safe',
            example_inputs=[{'value': 42}]
        )
        
        algorithms = clean_registry.list_algorithms()
        
        # Should not raise
        json_str = json.dumps(algorithms)
        assert isinstance(json_str, str)


# =============================================================================
# Test Group 7: Helper Methods and Convenience Functions
# =============================================================================

@pytest.mark.unit
class TestHelperMethods:
    """Test helper methods and convenience functions."""
    
    def test_is_registered_returns_true_for_registered(self, clean_registry, minimal_tracer):
        """is_registered returns True for registered algorithm."""
        clean_registry.register(
            name='registered',
            tracer_class=minimal_tracer.__class__,
            display_name='Registered',
            description='Test',
            example_inputs=[{}]
        )
        
        assert clean_registry.is_registered('registered') is True
    
    def test_is_registered_returns_false_for_unregistered(self, clean_registry):
        """is_registered returns False for unregistered algorithm."""
        assert clean_registry.is_registered('not-registered') is False
    
    def test_contains_operator(self, clean_registry, minimal_tracer):
        """'in' operator works with registry."""
        clean_registry.register(
            name='contains-test',
            tracer_class=minimal_tracer.__class__,
            display_name='Contains Test',
            description='Test',
            example_inputs=[{}]
        )
        
        assert 'contains-test' in clean_registry
        assert 'not-in-registry' not in clean_registry
    
    def test_len_operator(self, clean_registry, minimal_tracer):
        """len() operator works with registry."""
        assert len(clean_registry) == 0
        
        clean_registry.register(
            name='len-test-1',
            tracer_class=minimal_tracer.__class__,
            display_name='Len Test 1',
            description='Test',
            example_inputs=[{}]
        )
        
        assert len(clean_registry) == 1
        
        clean_registry.register(
            name='len-test-2',
            tracer_class=minimal_tracer.__class__,
            display_name='Len Test 2',
            description='Test',
            example_inputs=[{}]
        )
        
        assert len(clean_registry) == 2
    
    def test_count_method(self, clean_registry, minimal_tracer):
        """count() method returns number of registered algorithms."""
        assert clean_registry.count() == 0
        
        for i in range(3):
            clean_registry.register(
                name=f'count-test-{i}',
                tracer_class=minimal_tracer.__class__,
                display_name=f'Count Test {i}',
                description='Test',
                example_inputs=[{}]
            )
        
        assert clean_registry.count() == 3


# =============================================================================
# Test Group 8: Global Convenience Functions
# =============================================================================

@pytest.mark.unit
class TestGlobalConvenienceFunctions:
    """Test module-level convenience functions."""
    
    def test_get_algorithm_names_returns_list(self):
        """get_algorithm_names returns list of registered algorithm names."""
        names = get_algorithm_names()
        assert isinstance(names, list)
        assert len(names) > 0
    
    def test_get_algorithm_names_includes_expected(self):
        """get_algorithm_names includes pre-registered algorithms."""
        names = get_algorithm_names()
        assert 'binary-search' in names
        assert 'interval-coverage' in names
    
    def test_get_algorithm_function_retrieves_tracer(self):
        """get_algorithm() convenience function retrieves tracer class."""
        tracer_class = get_algorithm('binary-search')
        assert issubclass(tracer_class, AlgorithmTracer)
    
    def test_get_algorithm_function_raises_on_unknown(self):
        """get_algorithm() raises KeyError for unknown algorithm."""
        with pytest.raises(KeyError):
            get_algorithm('unknown-algorithm')


# =============================================================================
# Test Group 9: Integration with Actual Algorithms
# =============================================================================

@pytest.mark.integration
class TestRegistryIntegration:
    """Test registry with actual registered algorithms."""
    
    def test_global_registry_has_binary_search(self):
        """Global registry includes binary-search."""
        assert 'binary-search' in registry
        
        metadata = registry.get_metadata('binary-search')
        assert metadata['display_name'] == 'Binary Search'
        assert 'example_inputs' in metadata
        assert len(metadata['example_inputs']) > 0
    
    def test_global_registry_has_interval_coverage(self):
        """Global registry includes interval-coverage."""
        assert 'interval-coverage' in registry
        
        metadata = registry.get_metadata('interval-coverage')
        assert metadata['display_name'] == 'Interval Coverage'
        assert 'example_inputs' in metadata
        assert len(metadata['example_inputs']) > 0
    
    def test_retrieve_and_execute_binary_search(self):
        """Can retrieve and execute binary-search tracer."""
        tracer_class = registry.get('binary-search')
        tracer = tracer_class()
        
        result = tracer.execute({
            'array': [1, 3, 5, 7, 9],
            'target': 5
        })
        
        assert 'result' in result
        assert 'trace' in result
        assert 'metadata' in result
    
    def test_retrieve_and_execute_interval_coverage(self):
        """Can retrieve and execute interval-coverage tracer."""
        tracer_class = registry.get('interval-coverage')
        tracer = tracer_class()
        
        result = tracer.execute({
            'intervals': [
                {'id': 1, 'start': 100, 'end': 200, 'color': 'blue'},
                {'id': 2, 'start': 150, 'end': 250, 'color': 'green'}
            ]
        })
        
        assert 'result' in result
        assert 'trace' in result
        assert 'metadata' in result
    
    def test_all_registered_algorithms_have_metadata(self):
        """All registered algorithms have complete metadata."""
        algorithms = registry.list_algorithms()
        
        for algo in algorithms:
            assert 'name' in algo
            assert 'display_name' in algo
            assert 'description' in algo
            assert 'example_inputs' in algo
            # input_schema is optional
    
    def test_all_example_inputs_are_valid_structure(self):
        """All example inputs have proper structure."""
        algorithms = registry.list_algorithms()
        
        for algo in algorithms:
            assert isinstance(algo['example_inputs'], list)
            assert len(algo['example_inputs']) > 0
            
            for example in algo['example_inputs']:
                assert isinstance(example, dict)
                # Each example should have 'name' and 'input'
                # (based on registry.py registrations)


# =============================================================================
# Test Group 10: Edge Cases
# =============================================================================

@pytest.mark.edge_case
class TestRegistryEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_register_with_none_input_schema(self, clean_registry, minimal_tracer):
        """Registering with input_schema=None works."""
        clean_registry.register(
            name='none-schema',
            tracer_class=minimal_tracer.__class__,
            display_name='None Schema',
            description='Test',
            example_inputs=[{}],
            input_schema=None
        )
        
        metadata = clean_registry.get_metadata('none-schema')
        assert metadata['input_schema'] is None
    
    def test_register_with_empty_example_inputs(self, clean_registry, minimal_tracer):
        """Registering with empty example_inputs list works."""
        clean_registry.register(
            name='empty-examples',
            tracer_class=minimal_tracer.__class__,
            display_name='Empty Examples',
            description='Test',
            example_inputs=[]
        )
        
        metadata = clean_registry.get_metadata('empty-examples')
        assert metadata['example_inputs'] == []
    
    def test_algorithm_names_with_special_characters(self, clean_registry, minimal_tracer):
        """Algorithm names can contain hyphens and underscores."""
        names = ['my-algorithm', 'my_algorithm', 'algo-2024']
        
        for name in names:
            clean_registry.register(
                name=name,
                tracer_class=minimal_tracer.__class__,
                display_name=name.title(),
                description='Test',
                example_inputs=[{}]
            )
        
        for name in names:
            assert name in clean_registry
    
    def test_registry_isolated_between_instances(self, minimal_tracer):
        """Different registry instances are independent."""
        reg1 = AlgorithmRegistry()
        reg2 = AlgorithmRegistry()
        
        reg1.register(
            name='only-in-reg1',
            tracer_class=minimal_tracer.__class__,
            display_name='Reg1 Only',
            description='Test',
            example_inputs=[{}]
        )
        
        assert 'only-in-reg1' in reg1
        assert 'only-in-reg1' not in reg2
    
    def test_get_metadata_with_complex_input_schema(self, clean_registry, minimal_tracer):
        """Complex input schemas are stored and retrieved correctly."""
        complex_schema = {
            'type': 'object',
            'required': ['array', 'target'],
            'properties': {
                'array': {
                    'type': 'array',
                    'items': {'type': 'integer'},
                    'minItems': 1
                },
                'target': {
                    'type': 'integer'
                }
            }
        }
        
        clean_registry.register(
            name='complex-schema',
            tracer_class=minimal_tracer.__class__,
            display_name='Complex Schema',
            description='Test',
            example_inputs=[{}],
            input_schema=complex_schema
        )
        
        metadata = clean_registry.get_metadata('complex-schema')
        assert metadata['input_schema'] == complex_schema
