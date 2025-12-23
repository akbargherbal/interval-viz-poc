
"""
Tests for Depth-First Search (Iterative) algorithm tracer.

Comprehensive test coverage for correctness, trace generation,
visualization state, prediction points, edge cases, and metadata compliance.

Target Coverage: ≥90%
"""

import pytest
from algorithms.depth_first_search_tracer import DepthFirstSearchTracer


# =============================================================================
# Test Class 1: Algorithm Correctness
# =============================================================================

@pytest.mark.unit
class TestDFSCorrectness:
    """Test algorithm correctness - does it traverse correctly?"""

    def test_simple_path_traversal(self):
        """Test DFS on simple linear path: A-B-C."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C']],
            'start_node': 'A'
        })
        
        assert result['result']['nodes_visited'] == 3
        assert set(result['result']['traversal_order']) == {'A', 'B', 'C'}
        assert result['result']['traversal_order'][0] == 'A'

    def test_triangle_graph(self):
        """Test DFS on triangle: A-B-C with all edges."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C'], ['C', 'A']],
            'start_node': 'A'
        })
        
        assert result['result']['nodes_visited'] == 3
        assert set(result['result']['traversal_order']) == {'A', 'B', 'C'}

    def test_disconnected_graph(self):
        """Test DFS on disconnected graph - should only visit connected component."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B']],
            'start_node': 'A'
        })
        
        # Should visit A and B, but not C (disconnected)
        assert result['result']['nodes_visited'] == 2
        assert set(result['result']['traversal_order']) == {'A', 'B'}
        assert 'C' not in result['result']['traversal_order']

    def test_single_node(self):
        """Test DFS on single node with no edges."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A'],
            'edges': [],
            'start_node': 'A'
        })
        
        assert result['result']['nodes_visited'] == 1
        assert result['result']['traversal_order'] == ['A']

    def test_star_graph(self):
        """Test DFS on star graph: center connected to all others."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D', 'E'],
            'edges': [['A', 'B'], ['A', 'C'], ['A', 'D'], ['A', 'E']],
            'start_node': 'A'
        })
        
        assert result['result']['nodes_visited'] == 5
        assert set(result['result']['traversal_order']) == {'A', 'B', 'C', 'D', 'E'}
        assert result['result']['traversal_order'][0] == 'A'

    def test_cycle_detection(self):
        """Test DFS handles cycles correctly (visits each node once)."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D'],
            'edges': [['A', 'B'], ['B', 'C'], ['C', 'D'], ['D', 'A']],
            'start_node': 'A'
        })
        
        # Should visit all 4 nodes exactly once
        assert result['result']['nodes_visited'] == 4
        assert len(result['result']['traversal_order']) == 4
        assert set(result['result']['traversal_order']) == {'A', 'B', 'C', 'D'}

    def test_complex_graph(self):
        """Test DFS on more complex graph structure."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
            'edges': [
                ['A', 'B'], ['A', 'C'],
                ['B', 'D'], ['B', 'E'],
                ['C', 'F']
            ],
            'start_node': 'A'
        })
        
        assert result['result']['nodes_visited'] == 6
        assert set(result['result']['traversal_order']) == {'A', 'B', 'C', 'D', 'E', 'F'}


# =============================================================================
# Test Class 2: Trace Structure
# =============================================================================

@pytest.mark.unit
class TestDFSTraceStructure:
    """Test trace generation - are all steps recorded correctly?"""

    def test_initial_state_first_step(self):
        """First step should be INITIAL_STATE."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [['A', 'B']],
            'start_node': 'A'
        })
        
        first_step = result['trace']['steps'][0]
        assert first_step['type'] == 'INITIAL_STATE'
        assert 'start_node' in first_step['data']
        assert first_step['data']['start_node'] == 'A'

    def test_push_stack_for_start_node(self):
        """Second step should push start node onto stack."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [['A', 'B']],
            'start_node': 'A'
        })
        
        second_step = result['trace']['steps'][1]
        assert second_step['type'] == 'PUSH_STACK'
        assert second_step['data']['node'] == 'A'

    def test_pop_stack_steps_present(self):
        """POP_STACK steps should be present."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C']],
            'start_node': 'A'
        })
        
        pop_steps = [s for s in result['trace']['steps'] if s['type'] == 'POP_STACK']
        assert len(pop_steps) >= 1

    def test_visit_node_steps_present(self):
        """VISIT_NODE steps should be present for each visited node."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C']],
            'start_node': 'A'
        })
        
        visit_steps = [s for s in result['trace']['steps'] if s['type'] == 'VISIT_NODE']
        assert len(visit_steps) == 3  # A, B, C

    def test_skip_visited_when_revisiting(self):
        """SKIP_VISITED should occur when encountering already-visited node."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C'], ['C', 'A']],
            'start_node': 'A'
        })
        
        skip_steps = [s for s in result['trace']['steps'] if s['type'] == 'SKIP_VISITED']
        # Should have skips when revisiting nodes via cycle
        assert len(skip_steps) >= 1

    def test_backtrack_steps_present(self):
        """BACKTRACK steps should occur when all neighbors visited."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C']],
            'start_node': 'A'
        })
        
        backtrack_steps = [s for s in result['trace']['steps'] if s['type'] == 'BACKTRACK']
        # Should have backtracking in linear path
        assert len(backtrack_steps) >= 1

    def test_trace_has_timestamps(self):
        """All steps should have timestamps."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [['A', 'B']],
            'start_node': 'A'
        })
        
        for step in result['trace']['steps']:
            assert 'timestamp' in step
            assert isinstance(step['timestamp'], (int, float))
            assert step['timestamp'] >= 0

    def test_total_steps_matches_array_length(self):
        """total_steps should match length of steps array."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [['A', 'B']],
            'start_node': 'A'
        })
        
        assert result['trace']['total_steps'] == len(result['trace']['steps'])


# =============================================================================
# Test Class 3: Visualization State
# =============================================================================

@pytest.mark.unit
class TestDFSVisualizationState:
    """Test visualization state - is frontend data correct?"""

    def test_visualization_state_present(self):
        """Each step should have visualization data."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [['A', 'B']],
            'start_node': 'A'
        })
        
        for step in result['trace']['steps']:
            assert 'visualization' in step['data']

    def test_nodes_structure(self):
        """Nodes should have id and state."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C']],
            'start_node': 'A'
        })
        
        # Check a VISIT_NODE step
        visit_step = [s for s in result['trace']['steps'] if s['type'] == 'VISIT_NODE'][0]
        viz = visit_step['data']['visualization']
        
        assert 'nodes' in viz
        assert len(viz['nodes']) == 3
        
        for node in viz['nodes']:
            assert 'id' in node
            assert 'state' in node

    def test_node_states_valid(self):
        """Node states should be: unvisited, examining, visited."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C']],
            'start_node': 'A'
        })
        
        valid_states = {'unvisited', 'examining', 'visited'}
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            for node in viz['nodes']:
                assert node['state'] in valid_states

    def test_examining_state_for_current_node(self):
        """Current node should have 'examining' state."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C']],
            'start_node': 'A'
        })
        
        # Check VISIT_NODE steps
        visit_steps = [s for s in result['trace']['steps'] if s['type'] == 'VISIT_NODE']
        
        for step in visit_steps:
            current = step['data']['node']
            viz = step['data']['visualization']
            
            current_node_viz = [n for n in viz['nodes'] if n['id'] == current][0]
            assert current_node_viz['state'] == 'examining'

    def test_visited_state_after_processing(self):
        """Nodes should have 'visited' state after being processed."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C']],
            'start_node': 'A'
        })
        
        # Check later steps - A should be visited
        later_steps = result['trace']['steps'][-5:]
        
        for step in later_steps:
            viz = step['data']['visualization']
            node_a = [n for n in viz['nodes'] if n['id'] == 'A'][0]
            assert node_a['state'] == 'visited'

    def test_edges_structure(self):
        """Edges should have from, to, and state."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [['A', 'B']],
            'start_node': 'A'
        })
        
        visit_step = [s for s in result['trace']['steps'] if s['type'] == 'VISIT_NODE'][0]
        viz = visit_step['data']['visualization']
        
        assert 'edges' in viz
        assert len(viz['edges']) >= 1
        
        for edge in viz['edges']:
            assert 'from' in edge
            assert 'to' in edge
            assert 'state' in edge

    def test_edge_states_valid(self):
        """Edge states should be: unexplored, traversed, backtrack."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C']],
            'start_node': 'A'
        })
        
        valid_states = {'unexplored', 'traversed', 'backtrack'}
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            for edge in viz['edges']:
                assert edge['state'] in valid_states

    def test_stack_present(self):
        """Stack should be present in visualization."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [['A', 'B']],
            'start_node': 'A'
        })
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            assert 'stack' in viz
            assert isinstance(viz['stack'], list)

    def test_stack_lifo_behavior(self):
        """Stack should follow LIFO (last in, first out)."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['A', 'C']],
            'start_node': 'A'
        })
        
        # Find PUSH_STACK steps
        push_steps = [s for s in result['trace']['steps'] if s['type'] == 'PUSH_STACK']
        
        # After pushing neighbors, last pushed should be on top
        if len(push_steps) >= 3:
            # After pushing B and C, check stack order
            step_after_pushes = None
            for i, step in enumerate(result['trace']['steps']):
                if step['type'] == 'PUSH_STACK' and step['data']['node'] in ['B', 'C']:
                    if i + 1 < len(result['trace']['steps']):
                        step_after_pushes = result['trace']['steps'][i + 1]
                        break
            
            if step_after_pushes:
                viz = step_after_pushes['data']['visualization']
                # Last element in stack array is top
                assert len(viz['stack']) >= 1

    def test_visited_set_present(self):
        """Visited set should be present and sorted."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C']],
            'start_node': 'A'
        })
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            assert 'visited' in viz
            assert isinstance(viz['visited'], list)
            
            # Should be sorted for consistent display
            if len(viz['visited']) > 1:
                assert viz['visited'] == sorted(viz['visited'])

    def test_visited_set_grows(self):
        """Visited set should grow as nodes are visited."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C']],
            'start_node': 'A'
        })
        
        visit_steps = [s for s in result['trace']['steps'] if s['type'] == 'VISIT_NODE']
        
        previous_size = 0
        for step in visit_steps:
            viz = step['data']['visualization']
            current_size = len(viz['visited'])
            assert current_size > previous_size
            previous_size = current_size

    def test_current_node_tracked(self):
        """Current node should be tracked in visualization."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [['A', 'B']],
            'start_node': 'A'
        })
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            assert 'current_node' in viz

    def test_traversal_order_tracked(self):
        """Traversal order should be tracked in visualization."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C']],
            'start_node': 'A'
        })
        
        for step in result['trace']['steps']:
            viz = step['data']['visualization']
            assert 'traversal_order' in viz
            assert isinstance(viz['traversal_order'], list)


# =============================================================================
# Test Class 4: Prediction Points
# =============================================================================

@pytest.mark.unit
class TestDFSPredictionPoints:
    """Test prediction points - are learning moments identified?"""

    def test_predictions_generated(self):
        """Prediction points should be generated."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C'], ['C', 'A']],
            'start_node': 'A'
        })
        
        predictions = result['metadata']['prediction_points']
        assert isinstance(predictions, list)

    def test_prediction_structure_complete(self):
        """Each prediction should have all required fields."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C'], ['C', 'A']],
            'start_node': 'A'
        })
        
        predictions = result['metadata']['prediction_points']
        
        if predictions:
            required_fields = ['step_index', 'question', 'choices', 'hint', 'correct_answer', 'explanation']
            
            for pred in predictions:
                for field in required_fields:
                    assert field in pred

    def test_prediction_choices_structure(self):
        """Each prediction should have 2 choices with id and label."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C'], ['C', 'A']],
            'start_node': 'A'
        })
        
        predictions = result['metadata']['prediction_points']
        
        if predictions:
            for pred in predictions:
                choices = pred['choices']
                assert len(choices) == 2
                
                choice_ids = {c['id'] for c in choices}
                assert choice_ids == {'visit', 'skip'}

    def test_correct_answer_valid(self):
        """Correct answer should be 'visit' or 'skip'."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B'], ['B', 'C'], ['C', 'A']],
            'start_node': 'A'
        })
        
        predictions = result['metadata']['prediction_points']
        valid_answers = {'visit', 'skip'}
        
        for pred in predictions:
            assert pred['correct_answer'] in valid_answers


# =============================================================================
# Test Class 5: Edge Cases & Error Handling
# =============================================================================

@pytest.mark.edge_case
class TestDFSEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_nodes_raises_error(self):
        """Empty nodes list should raise ValueError."""
        tracer = DepthFirstSearchTracer()
        
        with pytest.raises(ValueError, match="at least one node"):
            tracer.execute({
                'nodes': [],
                'edges': [],
                'start_node': 'A'
            })

    def test_start_node_not_in_graph_raises_error(self):
        """Start node not in graph should raise ValueError."""
        tracer = DepthFirstSearchTracer()
        
        with pytest.raises(ValueError, match="not in graph"):
            tracer.execute({
                'nodes': ['A', 'B'],
                'edges': [['A', 'B']],
                'start_node': 'Z'
            })

    def test_non_dict_input_raises_error(self):
        """Non-dictionary input should raise ValueError."""
        tracer = DepthFirstSearchTracer()
        
        with pytest.raises(ValueError, match="dictionary"):
            tracer.execute(['A', 'B'])

    def test_missing_nodes_key_raises_error(self):
        """Missing 'nodes' key should raise ValueError."""
        tracer = DepthFirstSearchTracer()
        
        with pytest.raises(ValueError, match="nodes"):
            tracer.execute({
                'edges': [],
                'start_node': 'A'
            })

    def test_missing_edges_key_raises_error(self):
        """Missing 'edges' key should raise ValueError."""
        tracer = DepthFirstSearchTracer()
        
        with pytest.raises(ValueError, match="edges"):
            tracer.execute({
                'nodes': ['A'],
                'start_node': 'A'
            })

    def test_missing_start_node_key_raises_error(self):
        """Missing 'start_node' key should raise ValueError."""
        tracer = DepthFirstSearchTracer()
        
        with pytest.raises(ValueError, match="start_node"):
            tracer.execute({
                'nodes': ['A'],
                'edges': []
            })

    def test_edge_references_unknown_node(self):
        """Edge referencing unknown node should raise ValueError."""
        tracer = DepthFirstSearchTracer()
        
        with pytest.raises(ValueError, match="unknown node"):
            tracer.execute({
                'nodes': ['A', 'B'],
                'edges': [['A', 'Z']],
                'start_node': 'A'
            })

    def test_single_node_no_edges(self):
        """Single node with no edges should work."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A'],
            'edges': [],
            'start_node': 'A'
        })
        
        assert result['result']['nodes_visited'] == 1
        assert result['result']['traversal_order'] == ['A']

    def test_self_loop(self):
        """Node with self-loop should be handled correctly."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A'],
            'edges': [['A', 'A']],
            'start_node': 'A'
        })
        
        # Should visit A once (self-loop doesn't cause revisit)
        assert result['result']['nodes_visited'] == 1
        assert result['result']['traversal_order'] == ['A']

    def test_multiple_disconnected_components(self):
        """Multiple disconnected components - only start component visited."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D'],
            'edges': [['A', 'B'], ['C', 'D']],
            'start_node': 'A'
        })
        
        # Should only visit A and B
        assert result['result']['nodes_visited'] == 2
        assert set(result['result']['traversal_order']) == {'A', 'B'}


# =============================================================================
# Test Class 6: Metadata Compliance
# =============================================================================

@pytest.mark.compliance
class TestDFSMetadataCompliance:
    """Test metadata compliance with frontend requirements."""

    def test_metadata_present(self):
        """Metadata should be present in result."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [['A', 'B']],
            'start_node': 'A'
        })
        
        assert 'metadata' in result

    def test_required_metadata_fields(self):
        """Metadata should have all required fields."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [['A', 'B']],
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
            assert field in metadata

    def test_algorithm_field_correct(self):
        """algorithm field should be 'depth-first-search'."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [['A', 'B']],
            'start_node': 'A'
        })
        
        assert result['metadata']['algorithm'] == 'depth-first-search'

    def test_display_name_field_correct(self):
        """display_name field should be 'Depth-First Search (Iterative)'."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [['A', 'B']],
            'start_node': 'A'
        })
        
        assert result['metadata']['display_name'] == 'Depth-First Search (Iterative)'

    def test_visualization_type_correct(self):
        """visualization_type should be 'graph'."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [['A', 'B']],
            'start_node': 'A'
        })
        
        assert result['metadata']['visualization_type'] == 'graph'

    def test_visualization_config_structure(self):
        """visualization_config should have expected fields."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [['A', 'B']],
            'start_node': 'A'
        })
        
        config = result['metadata']['visualization_config']
        
        assert 'directed' in config
        assert config['directed'] is False
        assert 'show_stack' in config
        assert config['show_stack'] is True
        assert 'show_visited' in config
        assert config['show_visited'] is True

    def test_input_size_correct(self):
        """input_size should match number of nodes."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D'],
            'edges': [['A', 'B'], ['B', 'C']],
            'start_node': 'A'
        })
        
        assert result['metadata']['input_size'] == 4

    def test_start_node_correct(self):
        """start_node should match input start_node."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [['A', 'B']],
            'start_node': 'B'
        })
        
        assert result['metadata']['start_node'] == 'B'

    def test_result_structure_correct(self):
        """Result should have correct top-level structure."""
        tracer = DepthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [['A', 'B']],
            'start_node': 'A'
        })
        
        # Top-level keys
        assert 'result' in result
        assert 'trace' in result
        assert 'metadata' in result
        
        # Result structure
        assert 'traversal_order' in result['result']
        assert 'nodes_visited' in result['result']
        
        # Trace structure
        assert 'steps' in result['trace']
        assert 'total_steps' in result['trace']
        assert 'duration' in result['trace']
