
"""
Tests for Dijkstra's Algorithm tracer.

Comprehensive test coverage for correctness, trace generation,
visualization state, prediction points, edge cases, and metadata compliance.

Target Coverage: ≥90%
"""

import pytest
from algorithms.dijkstras_algorithm_tracer import DijkstrasAlgorithmTracer


# =============================================================================
# Test Class 1: Algorithm Correctness
# =============================================================================

@pytest.mark.unit
class TestDijkstrasAlgorithmCorrectness:
    """Test algorithm correctness - does it find the right shortest paths?"""

    def test_simple_path(self):
        """Test simple linear path A -> B -> C."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B', 5), ('B', 'C', 3)],
            'start_node': 'A'
        })
        
        distances = result['result']['distances']
        assert distances['A'] == 0
        assert distances['B'] == 5
        assert distances['C'] == 8
        
        paths = result['result']['paths']
        assert paths['A'] == ['A']
        assert paths['B'] == ['A', 'B']
        assert paths['C'] == ['A', 'B', 'C']

    def test_multiple_paths_chooses_shortest(self):
        """Test that algorithm chooses shortest path when multiple exist."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [
                ('A', 'B', 4),
                ('A', 'C', 2),
                ('C', 'B', 1)
            ],
            'start_node': 'A'
        })
        
        distances = result['result']['distances']
        assert distances['A'] == 0
        assert distances['B'] == 3  # Via C (2 + 1), not direct (4)
        assert distances['C'] == 2
        
        paths = result['result']['paths']
        assert paths['B'] == ['A', 'C', 'B']

    def test_unreachable_node(self):
        """Test handling of unreachable nodes."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        distances = result['result']['distances']
        assert distances['A'] == 0
        assert distances['B'] == 5
        assert distances['C'] is None  # Infinity serialized as None
        
        paths = result['result']['paths']
        assert paths['C'] == []  # Empty path for unreachable

    def test_single_node(self):
        """Test graph with single node."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A'],
            'edges': [],
            'start_node': 'A'
        })
        
        distances = result['result']['distances']
        assert distances['A'] == 0
        
        paths = result['result']['paths']
        assert paths['A'] == ['A']

    def test_disconnected_components(self):
        """Test graph with disconnected components."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D'],
            'edges': [
                ('A', 'B', 3),
                ('C', 'D', 2)
            ],
            'start_node': 'A'
        })
        
        distances = result['result']['distances']
        assert distances['A'] == 0
        assert distances['B'] == 3
        assert distances['C'] is None  # Unreachable
        assert distances['D'] is None  # Unreachable

    def test_triangle_graph(self):
        """Test triangle graph with all edges."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [
                ('A', 'B', 1),
                ('B', 'C', 2),
                ('A', 'C', 4)
            ],
            'start_node': 'A'
        })
        
        distances = result['result']['distances']
        assert distances['A'] == 0
        assert distances['B'] == 1
        assert distances['C'] == 3  # Via B (1 + 2), not direct (4)

    def test_larger_graph(self):
        """Test larger graph with 5 nodes."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D', 'E'],
            'edges': [
                ('A', 'B', 4),
                ('A', 'C', 2),
                ('B', 'C', 1),
                ('B', 'D', 5),
                ('C', 'D', 8),
                ('C', 'E', 10),
                ('D', 'E', 2)
            ],
            'start_node': 'A'
        })
        
        distances = result['result']['distances']
        assert distances['A'] == 0
        assert distances['B'] == 3  # Via C
        assert distances['C'] == 2
        assert distances['D'] == 8  # Via B
        assert distances['E'] == 10  # Via D


# =============================================================================
# Test Class 2: Trace Structure
# =============================================================================

@pytest.mark.unit
class TestDijkstrasAlgorithmTraceStructure:
    """Test trace generation - are all steps recorded correctly?"""

    def test_init_distances_first_step(self):
        """First step should be INIT_DISTANCES."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        first_step = result['trace']['steps'][0]
        assert first_step['type'] == 'INIT_DISTANCES'
        assert 'start_node' in first_step['data']
        assert first_step['data']['start_node'] == 'A'

    def test_select_min_dist_steps_present(self):
        """SELECT_MIN_DIST steps should be present."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B', 5), ('B', 'C', 3)],
            'start_node': 'A'
        })
        
        select_steps = [s for s in result['trace']['steps'] if s['type'] == 'SELECT_MIN_DIST']
        assert len(select_steps) == 3  # One for each node

    def test_visit_node_follows_select(self):
        """VISIT_NODE should follow SELECT_MIN_DIST."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        steps = result['trace']['steps']
        for i, step in enumerate(steps):
            if step['type'] == 'SELECT_MIN_DIST' and i + 1 < len(steps):
                next_step = steps[i + 1]
                assert next_step['type'] == 'VISIT_NODE'

    def test_check_neighbor_for_each_edge(self):
        """CHECK_NEIGHBOR should be recorded for each edge."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B', 5), ('A', 'C', 3)],
            'start_node': 'A'
        })
        
        check_steps = [s for s in result['trace']['steps'] if s['type'] == 'CHECK_NEIGHBOR']
        # Should check B and C from A
        assert len(check_steps) >= 2

    def test_relax_edge_steps_present(self):
        """RELAX_EDGE steps should be present."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        relax_steps = [s for s in result['trace']['steps'] if s['type'] == 'RELAX_EDGE']
        assert len(relax_steps) >= 1

    def test_update_distance_when_improved(self):
        """UPDATE_DISTANCE should follow RELAX_EDGE when improvement found."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        steps = result['trace']['steps']
        for i, step in enumerate(steps):
            if step['type'] == 'RELAX_EDGE' and step['data']['improved']:
                # Next step should be UPDATE_DISTANCE
                if i + 1 < len(steps):
                    next_step = steps[i + 1]
                    assert next_step['type'] == 'UPDATE_DISTANCE'

    def test_trace_has_timestamps(self):
        """All steps should have timestamps."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        for step in result['trace']['steps']:
            assert 'timestamp' in step
            assert isinstance(step['timestamp'], (int, float))
            assert step['timestamp'] >= 0

    def test_total_steps_matches_array_length(self):
        """total_steps should match length of steps array."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        assert result['trace']['total_steps'] == len(result['trace']['steps'])


# =============================================================================
# Test Class 3: Visualization State
# =============================================================================

@pytest.mark.unit
class TestDijkstrasAlgorithmVisualizationState:
    """Test visualization state - is frontend data correct?"""

    def test_visualization_state_present(self):
        """Each step should have visualization data."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        for step in result['trace']['steps']:
            assert 'visualization' in step['data']

    def test_nodes_structure(self):
        """Nodes should have id, state, distance, previous."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        # Check a step with visualization
        step = result['trace']['steps'][1]
        viz = step['data']['visualization']
        
        assert 'nodes' in viz
        for node in viz['nodes']:
            assert 'id' in node
            assert 'state' in node
            assert 'distance' in node
            assert 'previous' in node

    def test_node_states_valid(self):
        """Node states should be unvisited, examining, or visited."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        valid_states = {'unvisited', 'examining', 'visited'}
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            for node in viz['nodes']:
                assert node['state'] in valid_states

    def test_edges_structure(self):
        """Edges should have from, to, weight, state."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        step = result['trace']['steps'][1]
        viz = step['data']['visualization']
        
        assert 'edges' in viz
        for edge in viz['edges']:
            assert 'from' in edge
            assert 'to' in edge
            assert 'weight' in edge
            assert 'state' in edge

    def test_edge_states_valid(self):
        """Edge states should be unexplored, examining, or relaxed."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        valid_states = {'unexplored', 'examining', 'relaxed'}
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            for edge in viz['edges']:
                assert edge['state'] in valid_states

    def test_priority_queue_present(self):
        """Priority queue should be in visualization."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        step = result['trace']['steps'][1]
        viz = step['data']['visualization']
        
        assert 'priority_queue' in viz
        assert isinstance(viz['priority_queue'], list)

    def test_priority_queue_structure(self):
        """Priority queue entries should have distance and node."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B', 5), ('A', 'C', 3)],
            'start_node': 'A'
        })
        
        # Find a step where PQ is non-empty
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            if viz['priority_queue']:
                for entry in viz['priority_queue']:
                    assert 'distance' in entry
                    assert 'node' in entry
                break

    def test_distance_map_present(self):
        """Distance map should be in visualization."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        step = result['trace']['steps'][1]
        viz = step['data']['visualization']
        
        assert 'distance_map' in viz
        assert isinstance(viz['distance_map'], dict)

    def test_previous_map_present(self):
        """Previous map should be in visualization."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        step = result['trace']['steps'][1]
        viz = step['data']['visualization']
        
        assert 'previous_map' in viz
        assert isinstance(viz['previous_map'], dict)

    def test_visited_set_present(self):
        """Visited set should be in visualization."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        step = result['trace']['steps'][1]
        viz = step['data']['visualization']
        
        assert 'visited_set' in viz
        assert isinstance(viz['visited_set'], list)

    def test_current_node_present(self):
        """Current node should be in visualization."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        step = result['trace']['steps'][1]
        viz = step['data']['visualization']
        
        assert 'current_node' in viz


# =============================================================================
# Test Class 4: Prediction Points
# =============================================================================

@pytest.mark.unit
class TestDijkstrasAlgorithmPredictionPoints:
    """Test prediction points - are learning moments identified?"""

    def test_predictions_generated(self):
        """Prediction points should be generated."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B', 5), ('A', 'C', 3)],
            'start_node': 'A'
        })
        
        predictions = result['metadata']['prediction_points']
        assert isinstance(predictions, list)

    def test_prediction_structure_complete(self):
        """Each prediction should have all required fields."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B', 5), ('A', 'C', 3)],
            'start_node': 'A'
        })
        
        predictions = result['metadata']['prediction_points']
        
        if predictions:  # Only test if predictions exist
            required_fields = ['step_index', 'question', 'choices', 'hint', 'correct_answer', 'explanation']
            
            for pred in predictions:
                for field in required_fields:
                    assert field in pred, f"Missing field: {field}"

    def test_prediction_choices_max_three(self):
        """Each prediction should have at most 3 choices."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D'],
            'edges': [('A', 'B', 5), ('A', 'C', 3), ('A', 'D', 7)],
            'start_node': 'A'
        })
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            assert len(pred['choices']) <= 3

    def test_prediction_choices_structure(self):
        """Each choice should have id and label."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B', 5), ('A', 'C', 3)],
            'start_node': 'A'
        })
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            for choice in pred['choices']:
                assert 'id' in choice
                assert 'label' in choice

    def test_correct_answer_in_choices(self):
        """Correct answer should be one of the choice ids."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B', 5), ('A', 'C', 3)],
            'start_node': 'A'
        })
        
        predictions = result['metadata']['prediction_points']
        
        for pred in predictions:
            choice_ids = {c['id'] for c in pred['choices']}
            assert pred['correct_answer'] in choice_ids


# =============================================================================
# Test Class 5: Edge Cases & Error Handling
# =============================================================================

@pytest.mark.edge_case
class TestDijkstrasAlgorithmEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_nodes_raises_error(self):
        """Empty nodes list should raise ValueError."""
        tracer = DijkstrasAlgorithmTracer()
        
        with pytest.raises(ValueError, match="cannot be empty"):
            tracer.execute({
                'nodes': [],
                'edges': [],
                'start_node': 'A'
            })

    def test_invalid_start_node_raises_error(self):
        """Start node not in nodes list should raise ValueError."""
        tracer = DijkstrasAlgorithmTracer()
        
        with pytest.raises(ValueError, match="not in nodes"):
            tracer.execute({
                'nodes': ['A', 'B'],
                'edges': [('A', 'B', 5)],
                'start_node': 'C'
            })

    def test_negative_weight_raises_error(self):
        """Negative edge weight should raise ValueError."""
        tracer = DijkstrasAlgorithmTracer()
        
        with pytest.raises(ValueError, match="Negative weight"):
            tracer.execute({
                'nodes': ['A', 'B'],
                'edges': [('A', 'B', -5)],
                'start_node': 'A'
            })

    def test_non_dict_input_raises_error(self):
        """Non-dictionary input should raise ValueError."""
        tracer = DijkstrasAlgorithmTracer()
        
        with pytest.raises(ValueError, match="dictionary"):
            tracer.execute(['A', 'B'])

    def test_missing_nodes_key_raises_error(self):
        """Missing 'nodes' key should raise ValueError."""
        tracer = DijkstrasAlgorithmTracer()
        
        with pytest.raises(ValueError, match="nodes"):
            tracer.execute({
                'edges': [],
                'start_node': 'A'
            })

    def test_missing_edges_key_raises_error(self):
        """Missing 'edges' key should raise ValueError."""
        tracer = DijkstrasAlgorithmTracer()
        
        with pytest.raises(ValueError, match="edges"):
            tracer.execute({
                'nodes': ['A'],
                'start_node': 'A'
            })

    def test_missing_start_node_key_raises_error(self):
        """Missing 'start_node' key should raise ValueError."""
        tracer = DijkstrasAlgorithmTracer()
        
        with pytest.raises(ValueError, match="start_node"):
            tracer.execute({
                'nodes': ['A'],
                'edges': []
            })

    def test_single_node_no_edges(self):
        """Single node with no edges should work."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A'],
            'edges': [],
            'start_node': 'A'
        })
        
        assert result['result']['distances']['A'] == 0
        assert result['result']['paths']['A'] == ['A']

    def test_zero_weight_edge(self):
        """Zero weight edge should be handled correctly."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 0)],
            'start_node': 'A'
        })
        
        assert result['result']['distances']['B'] == 0

    def test_self_loop_ignored(self):
        """Self-loop should not affect shortest paths."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'A', 5), ('A', 'B', 3)],
            'start_node': 'A'
        })
        
        assert result['result']['distances']['A'] == 0
        assert result['result']['distances']['B'] == 3


# =============================================================================
# Test Class 6: Metadata Compliance
# =============================================================================

@pytest.mark.compliance
class TestDijkstrasAlgorithmMetadataCompliance:
    """Test metadata compliance with frontend requirements."""

    def test_metadata_present(self):
        """Metadata should be present in result."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        assert 'metadata' in result

    def test_required_metadata_fields(self):
        """Metadata should have all required fields."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        metadata = result['metadata']
        
        required_fields = [
            'algorithm',
            'display_name',
            'visualization_type',
            'visualization_config',
            'input_size',
            'start_node',
            'prediction_points'
        ]
        
        for field in required_fields:
            assert field in metadata, f"Missing required field: {field}"

    def test_algorithm_field_correct(self):
        """algorithm field should be 'dijkstras-algorithm'."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        assert result['metadata']['algorithm'] == 'dijkstras-algorithm'

    def test_display_name_field_correct(self):
        """display_name field should be 'Dijkstra's Algorithm'."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        assert result['metadata']['display_name'] == "Dijkstra's Algorithm"

    def test_visualization_type_correct(self):
        """visualization_type should be 'graph'."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        assert result['metadata']['visualization_type'] == 'graph'

    def test_visualization_config_structure(self):
        """visualization_config should have expected fields."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        config = result['metadata']['visualization_config']
        
        assert 'directed' in config
        assert config['directed'] is False
        assert 'weighted' in config
        assert config['weighted'] is True
        assert 'show_priority_queue' in config
        assert config['show_priority_queue'] is True
        assert 'show_distances' in config
        assert config['show_distances'] is True

    def test_input_size_correct(self):
        """input_size should match number of nodes."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        assert result['metadata']['input_size'] == 3

    def test_start_node_in_metadata(self):
        """start_node should be in metadata."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        assert result['metadata']['start_node'] == 'A'

    def test_result_structure_correct(self):
        """Result should have correct top-level structure."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        # Top-level keys
        assert 'result' in result
        assert 'trace' in result
        assert 'metadata' in result
        
        # Result structure
        assert 'distances' in result['result']
        assert 'paths' in result['result']
        
        # Trace structure
        assert 'steps' in result['trace']
        assert 'total_steps' in result['trace']
        assert 'duration' in result['trace']


# =============================================================================
# Test Class 7: Narrative Generation
# =============================================================================

@pytest.mark.unit
class TestDijkstrasAlgorithmNarrative:
    """Test narrative generation."""

    def test_narrative_generation_executes(self):
        """Narrative generation should execute without errors."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B', 5), ('B', 'C', 3)],
            'start_node': 'A'
        })
        
        # Should not raise exception
        narrative = tracer.generate_narrative(result)
        assert isinstance(narrative, str)
        assert len(narrative) > 0

    def test_narrative_includes_header(self):
        """Narrative should include header with algorithm name."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        narrative = tracer.generate_narrative(result)
        assert "Dijkstra's Algorithm" in narrative

    def test_narrative_includes_visualization_hints(self):
        """Narrative should include Frontend Visualization Hints section."""
        tracer = DijkstrasAlgorithmTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B', 5)],
            'start_node': 'A'
        })
        
        narrative = tracer.generate_narrative(result)
        assert "🎨 Frontend Visualization Hints" in narrative
        assert "Primary Metrics to Emphasize" in narrative
        assert "Visualization Priorities" in narrative
        assert "Key JSON Paths" in narrative
        assert "Algorithm-Specific Guidance" in narrative
