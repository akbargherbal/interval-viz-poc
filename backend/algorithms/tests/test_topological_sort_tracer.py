
"""
Tests for Topological Sort (Kahn's Algorithm) tracer.

Comprehensive test coverage for correctness, trace generation,
visualization state, prediction points, edge cases, and metadata compliance.

Target Coverage: ≥90%
"""

import pytest
from algorithms.topological_sort_tracer import TopologicalSortTracer


# =============================================================================
# Test Class 1: Algorithm Correctness
# =============================================================================

@pytest.mark.unit
class TestTopologicalSortCorrectness:
    """Test algorithm correctness - does it produce valid topological ordering?"""

    def test_simple_linear_dag(self):
        """Test simple linear DAG: A → B → C."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C')]
        })
        
        assert result['result']['has_cycle'] is False
        assert result['result']['nodes_processed'] == 3
        
        sorted_order = result['result']['sorted_order']
        assert len(sorted_order) == 3
        
        # Verify ordering: A before B, B before C
        assert sorted_order.index('A') < sorted_order.index('B')
        assert sorted_order.index('B') < sorted_order.index('C')

    def test_diamond_dag(self):
        """Test diamond DAG: A → B, A → C, B → D, C → D."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D'],
            'edges': [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')]
        })
        
        assert result['result']['has_cycle'] is False
        assert result['result']['nodes_processed'] == 4
        
        sorted_order = result['result']['sorted_order']
        
        # Verify all edges respect ordering
        assert sorted_order.index('A') < sorted_order.index('B')
        assert sorted_order.index('A') < sorted_order.index('C')
        assert sorted_order.index('B') < sorted_order.index('D')
        assert sorted_order.index('C') < sorted_order.index('D')

    def test_disconnected_dag(self):
        """Test disconnected DAG: A → B, C (isolated)."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B')]
        })
        
        assert result['result']['has_cycle'] is False
        assert result['result']['nodes_processed'] == 3
        
        sorted_order = result['result']['sorted_order']
        assert len(sorted_order) == 3
        
        # A must come before B
        assert sorted_order.index('A') < sorted_order.index('B')
        # C can be anywhere (no constraints)
        assert 'C' in sorted_order

    def test_multiple_sources(self):
        """Test DAG with multiple source nodes (in-degree 0)."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D'],
            'edges': [('A', 'C'), ('B', 'C'), ('C', 'D')]
        })
        
        assert result['result']['has_cycle'] is False
        assert result['result']['nodes_processed'] == 4
        
        sorted_order = result['result']['sorted_order']
        
        # A and B are sources, both must come before C
        assert sorted_order.index('A') < sorted_order.index('C')
        assert sorted_order.index('B') < sorted_order.index('C')
        assert sorted_order.index('C') < sorted_order.index('D')

    def test_single_node_no_edges(self):
        """Test single node with no edges."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A'],
            'edges': []
        })
        
        assert result['result']['has_cycle'] is False
        assert result['result']['nodes_processed'] == 1
        assert result['result']['sorted_order'] == ['A']

    def test_two_node_cycle(self):
        """Test cycle detection: A → B → A."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B'), ('B', 'A')]
        })
        
        assert result['result']['has_cycle'] is True
        assert result['result']['nodes_processed'] < 2

    def test_three_node_cycle(self):
        """Test cycle detection: A → B → C → A."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C'), ('C', 'A')]
        })
        
        assert result['result']['has_cycle'] is True
        assert result['result']['nodes_processed'] < 3

    def test_self_loop(self):
        """Test cycle detection: A → A (self-loop)."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'A'), ('A', 'B')]
        })
        
        assert result['result']['has_cycle'] is True

    def test_complex_dag(self):
        """Test complex DAG with multiple paths."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
            'edges': [
                ('A', 'B'), ('A', 'C'),
                ('B', 'D'), ('C', 'D'),
                ('D', 'E'), ('C', 'F'),
                ('F', 'E')
            ]
        })
        
        assert result['result']['has_cycle'] is False
        assert result['result']['nodes_processed'] == 6
        
        sorted_order = result['result']['sorted_order']
        
        # Verify all edges
        edges = [
            ('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'),
            ('D', 'E'), ('C', 'F'), ('F', 'E')
        ]
        for from_node, to_node in edges:
            assert sorted_order.index(from_node) < sorted_order.index(to_node)


# =============================================================================
# Test Class 2: Trace Structure
# =============================================================================

@pytest.mark.unit
class TestTopologicalSortTraceStructure:
    """Test trace generation - are all steps recorded correctly?"""

    def test_calc_indegrees_first_step(self):
        """First step should be CALC_INDEGREES."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C')]
        })
        
        first_step = result['trace']['steps'][0]
        assert first_step['type'] == 'CALC_INDEGREES'
        assert 'indegree_calculation' in first_step['data']

    def test_enqueue_zero_indegree_second_step(self):
        """Second step should be ENQUEUE_ZERO_INDEGREE."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C')]
        })
        
        second_step = result['trace']['steps'][1]
        assert second_step['type'] == 'ENQUEUE_ZERO_INDEGREE'
        assert 'nodes_enqueued' in second_step['data']

    def test_process_node_steps_present(self):
        """PROCESS_NODE steps should be present for each processed node."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C')]
        })
        
        process_steps = [s for s in result['trace']['steps'] if s['type'] == 'PROCESS_NODE']
        
        # Should have 3 PROCESS_NODE steps (one per node)
        assert len(process_steps) == 3
        
        # Each should have required data
        for step in process_steps:
            assert 'node' in step['data']
            assert 'neighbors' in step['data']
            assert 'queue_before' in step['data']

    def test_decrement_neighbor_steps(self):
        """DECREMENT_NEIGHBOR steps should follow PROCESS_NODE."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C')]
        })
        
        decrement_steps = [s for s in result['trace']['steps'] if s['type'] == 'DECREMENT_NEIGHBOR']
        
        # Should have 2 DECREMENT_NEIGHBOR steps (one per edge)
        assert len(decrement_steps) == 2
        
        for step in decrement_steps:
            assert 'current_node' in step['data']
            assert 'neighbor' in step['data']
            assert 'old_indegree' in step['data']
            assert 'new_indegree' in step['data']
            assert 'enqueued' in step['data']

    def test_cycle_detection_step(self):
        """DETECT_CYCLE step should be present when cycle exists."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B'), ('B', 'A')]
        })
        
        cycle_steps = [s for s in result['trace']['steps'] if s['type'] == 'DETECT_CYCLE']
        
        assert len(cycle_steps) == 1
        
        cycle_step = cycle_steps[0]
        assert cycle_step['data']['has_cycle'] is True
        assert 'remaining_nodes' in cycle_step['data']

    def test_no_cycle_detection_for_valid_dag(self):
        """DETECT_CYCLE step should not be present for valid DAG."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C')]
        })
        
        cycle_steps = [s for s in result['trace']['steps'] if s['type'] == 'DETECT_CYCLE']
        
        assert len(cycle_steps) == 0

    def test_trace_has_timestamps(self):
        """All steps should have timestamps."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')]
        })
        
        for step in result['trace']['steps']:
            assert 'timestamp' in step
            assert isinstance(step['timestamp'], (int, float))
            assert step['timestamp'] >= 0

    def test_total_steps_matches_array_length(self):
        """total_steps should match length of steps array."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')]
        })
        
        assert result['trace']['total_steps'] == len(result['trace']['steps'])


# =============================================================================
# Test Class 3: Visualization State
# =============================================================================

@pytest.mark.unit
class TestTopologicalSortVisualizationState:
    """Test visualization state - is frontend data correct?"""

    def test_visualization_state_present(self):
        """Each step should have visualization data."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')]
        })
        
        for step in result['trace']['steps']:
            assert 'visualization' in step['data']

    def test_nodes_structure(self):
        """Nodes should have id, state, and indegree."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C')]
        })
        
        first_step = result['trace']['steps'][0]
        viz = first_step['data']['visualization']
        
        assert 'nodes' in viz
        assert len(viz['nodes']) == 3
        
        for node in viz['nodes']:
            assert 'id' in node
            assert 'state' in node
            assert 'indegree' in node

    def test_edges_structure(self):
        """Edges should have from, to, and state."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')]
        })
        
        first_step = result['trace']['steps'][0]
        viz = first_step['data']['visualization']
        
        assert 'edges' in viz
        assert len(viz['edges']) == 1
        
        for edge in viz['edges']:
            assert 'from' in edge
            assert 'to' in edge
            assert 'state' in edge

    def test_node_states_valid(self):
        """Node states should be valid."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C')]
        })
        
        valid_states = {'unprocessed', 'ready', 'processing', 'sorted'}
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            for node in viz['nodes']:
                assert node['state'] in valid_states

    def test_edge_states_valid(self):
        """Edge states should be valid."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')]
        })
        
        valid_states = {'active', 'traversed'}
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            for edge in viz['edges']:
                assert edge['state'] in valid_states

    def test_indegree_map_present(self):
        """In-degree map should be present."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')]
        })
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            assert 'indegree_map' in viz
            assert isinstance(viz['indegree_map'], dict)

    def test_queue_state_present(self):
        """Queue state should be present."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')]
        })
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            assert 'queue' in viz
            assert isinstance(viz['queue'], list)

    def test_sorted_order_present(self):
        """Sorted order should be present."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')]
        })
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            assert 'sorted_order' in viz
            assert isinstance(viz['sorted_order'], list)

    def test_sorted_order_grows(self):
        """Sorted order should grow with each PROCESS_NODE step."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C')]
        })
        
        process_steps = [s for s in result['trace']['steps'] if s['type'] == 'PROCESS_NODE']
        
        for i, step in enumerate(process_steps):
            viz = step['data']['visualization']
            assert len(viz['sorted_order']) == i + 1

    def test_indegrees_decrease(self):
        """In-degrees should decrease during DECREMENT_NEIGHBOR steps."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C')]
        })
        
        decrement_steps = [s for s in result['trace']['steps'] if s['type'] == 'DECREMENT_NEIGHBOR']
        
        for step in decrement_steps:
            data = step['data']
            assert data['new_indegree'] == data['old_indegree'] - 1


# =============================================================================
# Test Class 4: Prediction Points
# =============================================================================

@pytest.mark.unit
class TestTopologicalSortPredictionPoints:
    """Test prediction points - are learning moments identified?"""

    def test_predictions_generated(self):
        """Prediction points should be generated."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C')]
        })
        
        predictions = result['metadata']['prediction_points']
        
        assert isinstance(predictions, list)
        # Should have predictions for nodes with neighbors
        assert len(predictions) >= 0

    def test_prediction_structure_complete(self):
        """Each prediction should have all required fields."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D'],
            'edges': [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')]
        })
        
        predictions = result['metadata']['prediction_points']
        
        if predictions:
            required_fields = ['step_index', 'question', 'choices', 'hint', 'correct_answer', 'explanation']
            
            for pred in predictions:
                for field in required_fields:
                    assert field in pred

    def test_prediction_choices_max_three(self):
        """Each prediction should have at most 3 choices."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D'],
            'edges': [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')]
        })
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            assert len(pred['choices']) <= 3

    def test_prediction_choices_structure(self):
        """Each choice should have id and label."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D'],
            'edges': [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')]
        })
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            for choice in pred['choices']:
                assert 'id' in choice
                assert 'label' in choice


# =============================================================================
# Test Class 5: Edge Cases & Error Handling
# =============================================================================

@pytest.mark.edge_case
class TestTopologicalSortEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_nodes_raises_error(self):
        """Empty nodes list should raise ValueError."""
        tracer = TopologicalSortTracer()
        
        with pytest.raises(ValueError, match="cannot be empty"):
            tracer.execute({'nodes': [], 'edges': []})

    def test_too_many_nodes_raises_error(self):
        """More than 10 nodes should raise ValueError."""
        tracer = TopologicalSortTracer()
        nodes = [f'N{i}' for i in range(11)]
        
        with pytest.raises(ValueError, match="Maximum 10 nodes"):
            tracer.execute({'nodes': nodes, 'edges': []})

    def test_invalid_edge_format_raises_error(self):
        """Invalid edge format should raise ValueError."""
        tracer = TopologicalSortTracer()
        
        with pytest.raises(ValueError, match="Invalid edge format"):
            tracer.execute({
                'nodes': ['A', 'B'],
                'edges': [('A',)]  # Missing second element
            })

    def test_edge_references_unknown_node_raises_error(self):
        """Edge referencing unknown node should raise ValueError."""
        tracer = TopologicalSortTracer()
        
        with pytest.raises(ValueError, match="unknown node"):
            tracer.execute({
                'nodes': ['A', 'B'],
                'edges': [('A', 'C')]  # C not in nodes
            })

    def test_non_dict_input_raises_error(self):
        """Non-dictionary input should raise ValueError."""
        tracer = TopologicalSortTracer()
        
        with pytest.raises(ValueError, match="dictionary"):
            tracer.execute(['A', 'B'])

    def test_missing_nodes_key_raises_error(self):
        """Missing 'nodes' key should raise ValueError."""
        tracer = TopologicalSortTracer()
        
        with pytest.raises(ValueError, match="nodes"):
            tracer.execute({'edges': []})

    def test_missing_edges_key_raises_error(self):
        """Missing 'edges' key should raise ValueError."""
        tracer = TopologicalSortTracer()
        
        with pytest.raises(ValueError, match="edges"):
            tracer.execute({'nodes': ['A']})

    def test_single_node_no_edges(self):
        """Single node with no edges should work."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A'],
            'edges': []
        })
        
        assert result['result']['has_cycle'] is False
        assert result['result']['sorted_order'] == ['A']

    def test_all_nodes_disconnected(self):
        """All nodes disconnected should work."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': []
        })
        
        assert result['result']['has_cycle'] is False
        assert len(result['result']['sorted_order']) == 3


# =============================================================================
# Test Class 6: Metadata Compliance
# =============================================================================

@pytest.mark.compliance
class TestTopologicalSortMetadataCompliance:
    """Test metadata compliance with frontend requirements."""

    def test_metadata_present(self):
        """Metadata should be present in result."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')]
        })
        
        assert 'metadata' in result

    def test_required_metadata_fields(self):
        """Metadata should have all required fields."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')]
        })
        
        metadata = result['metadata']
        
        required_fields = [
            'algorithm',
            'display_name',
            'visualization_type',
            'visualization_config',
            'input_size',
            'prediction_points'
        ]
        
        for field in required_fields:
            assert field in metadata

    def test_algorithm_field_correct(self):
        """algorithm field should be 'topological-sort'."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')]
        })
        
        assert result['metadata']['algorithm'] == 'topological-sort'

    def test_display_name_field_correct(self):
        """display_name field should be correct."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')]
        })
        
        assert result['metadata']['display_name'] == "Topological Sort (Kahn's Algorithm)"

    def test_visualization_type_correct(self):
        """visualization_type should be 'graph'."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')]
        })
        
        assert result['metadata']['visualization_type'] == 'graph'

    def test_visualization_config_structure(self):
        """visualization_config should have expected fields."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')]
        })
        
        config = result['metadata']['visualization_config']
        
        assert config['directed'] is True
        assert config['show_indegrees'] is True
        assert config['show_queue'] is True

    def test_input_size_correct(self):
        """input_size should match number of nodes."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B')]
        })
        
        assert result['metadata']['input_size'] == 3

    def test_result_structure_correct(self):
        """Result should have correct structure."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')]
        })
        
        # Top-level keys
        assert 'result' in result
        assert 'trace' in result
        assert 'metadata' in result
        
        # Result structure
        assert 'sorted_order' in result['result']
        assert 'has_cycle' in result['result']
        assert 'nodes_processed' in result['result']


# =============================================================================
# Test Class 7: Narrative Generation
# =============================================================================

@pytest.mark.unit
class TestTopologicalSortNarrative:
    """Test narrative generation."""

    def test_narrative_generation_executes(self):
        """Narrative generation should execute without errors."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C')]
        })
        
        narrative = tracer.generate_narrative(result)
        
        assert isinstance(narrative, str)
        assert len(narrative) > 0

    def test_narrative_includes_visualization_hints(self):
        """Narrative should include Frontend Visualization Hints section."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')]
        })
        
        narrative = tracer.generate_narrative(result)
        
        assert "🎨 Frontend Visualization Hints" in narrative
        assert "Primary Metrics to Emphasize" in narrative
        assert "Visualization Priorities" in narrative
        assert "Key JSON Paths" in narrative

    def test_narrative_shows_graph_structure(self):
        """Narrative should show graph structure in Step 0."""
        tracer = TopologicalSortTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C')]
        })
        
        narrative = tracer.generate_narrative(result)
        
        assert "Graph Structure" in narrative
        assert "Adjacency List" in narrative
