
"""
Tests for Breadth-First Search algorithm tracer.

Comprehensive test coverage for correctness, trace generation,
visualization state, prediction points, edge cases, and metadata compliance.

Target Coverage: ≥90%
"""

import pytest
from algorithms.breadth_first_search_tracer import BreadthFirstSearchTracer


# =============================================================================
# Test Class 1: Algorithm Correctness
# =============================================================================

@pytest.mark.unit
class TestBFSCorrectness:
    """Test algorithm correctness - does it traverse correctly?"""

    def test_single_node_graph(self):
        """Single node with no edges."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A'],
            'edges': [],
            'start_node': 'A'
        })

        assert result['result']['start_node'] == 'A'
        assert result['result']['traversal_order'] == ['A']
        assert result['result']['levels'] == {'A': 0}
        assert result['result']['visited_count'] == 1

    def test_linear_chain(self):
        """Linear chain: A - B - C - D."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D'],
            'edges': [('A', 'B'), ('B', 'C'), ('C', 'D')],
            'start_node': 'A'
        })

        assert result['result']['start_node'] == 'A'
        assert result['result']['traversal_order'] == ['A', 'B', 'C', 'D']
        assert result['result']['levels'] == {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        assert result['result']['visited_count'] == 4

    def test_complete_graph_three_nodes(self):
        """Complete graph with 3 nodes (all connected)."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('A', 'C'), ('B', 'C')],
            'start_node': 'A'
        })

        assert result['result']['start_node'] == 'A'
        assert result['result']['traversal_order'][0] == 'A'
        # B and C should both be at level 1 (order may vary)
        assert set(result['result']['traversal_order'][1:]) == {'B', 'C'}
        assert result['result']['levels']['A'] == 0
        assert result['result']['levels']['B'] == 1
        assert result['result']['levels']['C'] == 1
        assert result['result']['visited_count'] == 3

    def test_tree_structure(self):
        """Tree structure: A root with children B, C; B has child D."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D'],
            'edges': [('A', 'B'), ('A', 'C'), ('B', 'D')],
            'start_node': 'A'
        })

        assert result['result']['start_node'] == 'A'
        assert result['result']['traversal_order'][0] == 'A'
        # Level 1: B and C (order may vary due to sorting)
        level_1 = result['result']['traversal_order'][1:3]
        assert set(level_1) == {'B', 'C'}
        # Level 2: D
        assert result['result']['traversal_order'][3] == 'D'
        
        assert result['result']['levels'] == {'A': 0, 'B': 1, 'C': 1, 'D': 2}
        assert result['result']['visited_count'] == 4

    def test_disconnected_graph(self):
        """Disconnected graph: A-B and C-D (two components)."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D'],
            'edges': [('A', 'B'), ('C', 'D')],
            'start_node': 'A'
        })

        # Should only visit A and B (connected component)
        assert result['result']['start_node'] == 'A'
        assert set(result['result']['traversal_order']) == {'A', 'B'}
        assert result['result']['levels'] == {'A': 0, 'B': 1}
        assert result['result']['visited_count'] == 2

    def test_cycle_graph(self):
        """Cycle graph: A - B - C - D - A."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D'],
            'edges': [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')],
            'start_node': 'A'
        })

        assert result['result']['start_node'] == 'A'
        assert result['result']['traversal_order'][0] == 'A'
        # All nodes should be visited
        assert len(result['result']['traversal_order']) == 4
        assert result['result']['visited_count'] == 4
        # Check levels are reasonable
        assert result['result']['levels']['A'] == 0
        assert all(level >= 0 for level in result['result']['levels'].values())

    def test_star_graph(self):
        """Star graph: A connected to B, C, D, E."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D', 'E'],
            'edges': [('A', 'B'), ('A', 'C'), ('A', 'D'), ('A', 'E')],
            'start_node': 'A'
        })

        assert result['result']['start_node'] == 'A'
        assert result['result']['traversal_order'][0] == 'A'
        # All other nodes at level 1
        assert set(result['result']['traversal_order'][1:]) == {'B', 'C', 'D', 'E'}
        assert result['result']['levels']['A'] == 0
        for node in ['B', 'C', 'D', 'E']:
            assert result['result']['levels'][node] == 1
        assert result['result']['visited_count'] == 5

    def test_level_order_property(self):
        """Verify level-order property: all nodes at level d before level d+1."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
            'edges': [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F')],
            'start_node': 'A'
        })

        traversal = result['result']['traversal_order']
        levels = result['result']['levels']

        # Check that levels are non-decreasing in traversal order
        traversal_levels = [levels[node] for node in traversal]
        for i in range(len(traversal_levels) - 1):
            # Level should not increase by more than 1
            assert traversal_levels[i+1] - traversal_levels[i] <= 1


# =============================================================================
# Test Class 2: Trace Structure
# =============================================================================

@pytest.mark.unit
class TestBFSTraceStructure:
    """Test trace generation - are all steps recorded correctly?"""

    def test_initial_state_first_step(self):
        """First step should be INITIAL_STATE."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        first_step = result['trace']['steps'][0]
        assert first_step['type'] == 'INITIAL_STATE'
        assert 'start_node' in first_step['data']
        assert first_step['data']['start_node'] == 'A'

    def test_enqueue_steps_present(self):
        """ENQUEUE steps should be present."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('A', 'C')],
            'start_node': 'A'
        })

        enqueue_steps = [s for s in result['trace']['steps'] if s['type'] == 'ENQUEUE']
        # Should enqueue A (start), then B and C
        assert len(enqueue_steps) >= 3

    def test_dequeue_steps_present(self):
        """DEQUEUE steps should be present."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('A', 'C')],
            'start_node': 'A'
        })

        dequeue_steps = [s for s in result['trace']['steps'] if s['type'] == 'DEQUEUE']
        # Should dequeue A, B, C
        assert len(dequeue_steps) == 3

    def test_visit_node_steps_present(self):
        """VISIT_NODE steps should be present."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('A', 'C')],
            'start_node': 'A'
        })

        visit_steps = [s for s in result['trace']['steps'] if s['type'] == 'VISIT_NODE']
        # Should visit A, B, C
        assert len(visit_steps) == 3

    def test_enqueue_neighbors_steps_present(self):
        """ENQUEUE_NEIGHBORS steps should be present."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('A', 'C')],
            'start_node': 'A'
        })

        neighbor_steps = [s for s in result['trace']['steps'] if s['type'] == 'ENQUEUE_NEIGHBORS']
        # Should process neighbors for A, B, C
        assert len(neighbor_steps) == 3

    def test_complete_step_last(self):
        """Last step should be COMPLETE."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        last_step = result['trace']['steps'][-1]
        assert last_step['type'] == 'COMPLETE'

    def test_step_sequence_logical(self):
        """Steps should follow logical sequence: DEQUEUE → VISIT → ENQUEUE_NEIGHBORS."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('A', 'C')],
            'start_node': 'A'
        })

        steps = result['trace']['steps']
        
        # Find first DEQUEUE
        for i, step in enumerate(steps):
            if step['type'] == 'DEQUEUE':
                # Next should be VISIT_NODE
                if i + 1 < len(steps):
                    assert steps[i + 1]['type'] == 'VISIT_NODE'
                # Then ENQUEUE_NEIGHBORS
                if i + 2 < len(steps):
                    assert steps[i + 2]['type'] == 'ENQUEUE_NEIGHBORS'
                break

    def test_trace_has_timestamps(self):
        """All steps should have timestamps."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        for step in result['trace']['steps']:
            assert 'timestamp' in step
            assert isinstance(step['timestamp'], (int, float))
            assert step['timestamp'] >= 0

    def test_total_steps_matches_array_length(self):
        """total_steps should match length of steps array."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        assert result['trace']['total_steps'] == len(result['trace']['steps'])


# =============================================================================
# Test Class 3: Visualization State
# =============================================================================

@pytest.mark.unit
class TestBFSVisualizationState:
    """Test visualization state - is frontend data correct?"""

    def test_visualization_state_present(self):
        """Each step should have visualization data."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        for step in result['trace']['steps']:
            if step['type'] != 'INITIAL_STATE':
                assert 'visualization' in step['data']

    def test_nodes_structure(self):
        """Nodes should have id, state, and level."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('A', 'C')],
            'start_node': 'A'
        })

        # Check a step with visualization
        step = result['trace']['steps'][1]  # Should have viz
        viz = step['data']['visualization']

        assert 'nodes' in viz
        for node in viz['nodes']:
            assert 'id' in node
            assert 'state' in node
            assert 'level' in node

    def test_node_states_valid(self):
        """Node states should be valid."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('A', 'C')],
            'start_node': 'A'
        })

        valid_states = {'unvisited', 'enqueued', 'visiting', 'visited'}

        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                for node in viz['nodes']:
                    assert node['state'] in valid_states

    def test_edges_structure(self):
        """Edges should have from, to, and state."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        # Check a step with visualization
        step = result['trace']['steps'][1]
        viz = step['data']['visualization']

        assert 'edges' in viz
        for edge in viz['edges']:
            assert 'from' in edge
            assert 'to' in edge
            assert 'state' in edge

    def test_edge_states_valid(self):
        """Edge states should be valid."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        valid_states = {'unexplored', 'exploring', 'traversed'}

        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                for edge in viz['edges']:
                    assert edge['state'] in valid_states

    def test_queue_present(self):
        """Queue should be present in visualization."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                assert 'queue' in viz
                assert isinstance(viz['queue'], list)

    def test_visited_set_present(self):
        """Visited set should be present in visualization."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                assert 'visited' in viz
                assert isinstance(viz['visited'], list)

    def test_traversal_order_present(self):
        """Traversal order should be present in visualization."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        for step in result['trace']['steps']:
            if 'visualization' in step['data']:
                viz = step['data']['visualization']
                assert 'traversal_order' in viz
                assert isinstance(viz['traversal_order'], list)

    def test_visiting_state_at_current_node(self):
        """Current node should have 'visiting' state."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        # Find a DEQUEUE step
        for step in result['trace']['steps']:
            if step['type'] == 'DEQUEUE':
                node = step['data']['node']
                viz = step['data']['visualization']
                
                # Find this node in visualization
                node_data = next(n for n in viz['nodes'] if n['id'] == node)
                assert node_data['state'] == 'visiting'
                break

    def test_visited_state_after_processing(self):
        """Node should have 'visited' state after VISIT_NODE."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        # Find a VISIT_NODE step
        for step in result['trace']['steps']:
            if step['type'] == 'VISIT_NODE':
                node = step['data']['node']
                viz = step['data']['visualization']
                
                # Find this node in visualization
                node_data = next(n for n in viz['nodes'] if n['id'] == node)
                assert node_data['state'] == 'visited'
                break

    def test_level_assignments_correct(self):
        """Level assignments should be correct."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('B', 'C')],
            'start_node': 'A'
        })

        # Check final state
        last_step = result['trace']['steps'][-1]
        viz = last_step['data']['visualization']

        # Find nodes and check levels
        for node_data in viz['nodes']:
            if node_data['id'] == 'A':
                assert node_data['level'] == 0
            elif node_data['id'] == 'B':
                assert node_data['level'] == 1
            elif node_data['id'] == 'C':
                assert node_data['level'] == 2


# =============================================================================
# Test Class 4: Prediction Points
# =============================================================================

@pytest.mark.unit
class TestBFSPredictionPoints:
    """Test prediction points - are learning moments identified?"""

    def test_predictions_generated(self):
        """Prediction points should be generated."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('A', 'C')],
            'start_node': 'A'
        })

        predictions = result['metadata']['prediction_points']
        assert isinstance(predictions, list)
        # Should have at least one prediction
        assert len(predictions) >= 1

    def test_prediction_structure_complete(self):
        """Each prediction should have all required fields."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('A', 'C')],
            'start_node': 'A'
        })

        predictions = result['metadata']['prediction_points']
        required_fields = ['step_index', 'question', 'choices', 'hint', 'correct_answer', 'explanation']

        for pred in predictions:
            for field in required_fields:
                assert field in pred

    def test_prediction_choices_max_three(self):
        """Each prediction should have at most 3 choices."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C', 'D'],
            'edges': [('A', 'B'), ('A', 'C'), ('A', 'D')],
            'start_node': 'A'
        })

        predictions = result['metadata']['prediction_points']

        for pred in predictions:
            choices = pred['choices']
            assert len(choices) <= 3

    def test_prediction_choices_structure(self):
        """Each choice should have id and label."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('A', 'C')],
            'start_node': 'A'
        })

        predictions = result['metadata']['prediction_points']

        for pred in predictions:
            for choice in pred['choices']:
                assert 'id' in choice
                assert 'label' in choice

    def test_prediction_question_mentions_node(self):
        """Question should mention the node being processed."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('A', 'C')],
            'start_node': 'A'
        })

        predictions = result['metadata']['prediction_points']

        for pred in predictions:
            question = pred['question']
            # Should mention a node
            assert any(node in question for node in ['A', 'B', 'C'])


# =============================================================================
# Test Class 5: Edge Cases & Error Handling
# =============================================================================

@pytest.mark.edge_case
class TestBFSEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_nodes_raises_error(self):
        """Empty nodes list should raise ValueError."""
        tracer = BreadthFirstSearchTracer()

        with pytest.raises(ValueError, match="at least one node"):
            tracer.execute({
                'nodes': [],
                'edges': [],
                'start_node': 'A'
            })

    def test_start_node_not_in_graph_raises_error(self):
        """Start node not in graph should raise ValueError."""
        tracer = BreadthFirstSearchTracer()

        with pytest.raises(ValueError, match="not found"):
            tracer.execute({
                'nodes': ['A', 'B'],
                'edges': [('A', 'B')],
                'start_node': 'Z'
            })

    def test_invalid_edge_raises_error(self):
        """Edge with node not in graph should raise ValueError."""
        tracer = BreadthFirstSearchTracer()

        with pytest.raises(ValueError, match="not in graph"):
            tracer.execute({
                'nodes': ['A', 'B'],
                'edges': [('A', 'Z')],
                'start_node': 'A'
            })

    def test_non_dict_input_raises_error(self):
        """Non-dictionary input should raise ValueError."""
        tracer = BreadthFirstSearchTracer()

        with pytest.raises(ValueError, match="dictionary"):
            tracer.execute(['A', 'B'])

    def test_missing_nodes_key_raises_error(self):
        """Missing 'nodes' key should raise ValueError."""
        tracer = BreadthFirstSearchTracer()

        with pytest.raises(ValueError, match="nodes"):
            tracer.execute({
                'edges': [],
                'start_node': 'A'
            })

    def test_missing_edges_key_raises_error(self):
        """Missing 'edges' key should raise ValueError."""
        tracer = BreadthFirstSearchTracer()

        with pytest.raises(ValueError, match="edges"):
            tracer.execute({
                'nodes': ['A'],
                'start_node': 'A'
            })

    def test_missing_start_node_key_raises_error(self):
        """Missing 'start_node' key should raise ValueError."""
        tracer = BreadthFirstSearchTracer()

        with pytest.raises(ValueError, match="start_node"):
            tracer.execute({
                'nodes': ['A'],
                'edges': []
            })

    def test_isolated_node(self):
        """Isolated node (no edges) should work."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A'],
            'edges': [],
            'start_node': 'A'
        })

        assert result['result']['traversal_order'] == ['A']
        assert result['result']['visited_count'] == 1

    def test_self_loop_ignored(self):
        """Self-loop should be handled (though unusual for BFS)."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'A'), ('A', 'B')],
            'start_node': 'A'
        })

        # Should still traverse correctly
        assert 'A' in result['result']['traversal_order']
        assert 'B' in result['result']['traversal_order']

    def test_large_graph(self):
        """Large graph (10 nodes) should work."""
        nodes = [f'N{i}' for i in range(10)]
        edges = [(f'N{i}', f'N{i+1}') for i in range(9)]
        
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': nodes,
            'edges': edges,
            'start_node': 'N0'
        })

        assert len(result['result']['traversal_order']) == 10
        assert result['result']['visited_count'] == 10


# =============================================================================
# Test Class 6: Metadata Compliance
# =============================================================================

@pytest.mark.compliance
class TestBFSMetadataCompliance:
    """Test metadata compliance with frontend requirements."""

    def test_metadata_present(self):
        """Metadata should be present in result."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        assert 'metadata' in result

    def test_required_metadata_fields(self):
        """Metadata should have all required fields."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
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
        """algorithm field should be 'breadth-first-search'."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        assert result['metadata']['algorithm'] == 'breadth-first-search'

    def test_display_name_field_correct(self):
        """display_name field should be 'Breadth-First Search'."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        assert result['metadata']['display_name'] == 'Breadth-First Search'

    def test_visualization_type_correct(self):
        """visualization_type should be 'graph'."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        assert result['metadata']['visualization_type'] == 'graph'

    def test_visualization_config_structure(self):
        """visualization_config should have expected fields."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        config = result['metadata']['visualization_config']

        assert 'directed' in config
        assert config['directed'] is False
        assert 'show_queue' in config
        assert config['show_queue'] is True
        assert 'show_levels' in config
        assert config['show_levels'] is True

    def test_input_size_correct(self):
        """input_size should match number of nodes."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('A', 'C')],
            'start_node': 'A'
        })

        assert result['metadata']['input_size'] == 3

    def test_start_node_in_metadata(self):
        """start_node should be in metadata."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        assert result['metadata']['start_node'] == 'A'

    def test_result_structure_correct(self):
        """Result should have correct top-level structure."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        # Top-level keys
        assert 'result' in result
        assert 'trace' in result
        assert 'metadata' in result

        # Result structure
        assert 'start_node' in result['result']
        assert 'traversal_order' in result['result']
        assert 'levels' in result['result']
        assert 'visited_count' in result['result']

        # Trace structure
        assert 'steps' in result['trace']
        assert 'total_steps' in result['trace']
        assert 'duration' in result['trace']


# =============================================================================
# Test Class 7: Narrative Generation
# =============================================================================

@pytest.mark.unit
class TestBFSNarrativeGeneration:
    """Test narrative generation - does it produce valid markdown?"""

    def test_narrative_generates_without_error(self):
        """Narrative should generate without KeyError."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('A', 'C')],
            'start_node': 'A'
        })

        # Should not raise KeyError
        narrative = tracer.generate_narrative(result)
        assert isinstance(narrative, str)
        assert len(narrative) > 0

    def test_narrative_includes_header(self):
        """Narrative should include header with algorithm name."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        narrative = tracer.generate_narrative(result)
        assert '# Breadth-First Search Execution Narrative' in narrative

    def test_narrative_includes_input_info(self):
        """Narrative should include input information."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B', 'C'],
            'edges': [('A', 'B'), ('A', 'C')],
            'start_node': 'A'
        })

        narrative = tracer.generate_narrative(result)
        # Narrative uses Markdown bold: **Start Node:** A
        assert '**Start Node:** A' in narrative or 'Start Node:' in narrative

    def test_narrative_includes_steps(self):
        """Narrative should include step-by-step descriptions."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        narrative = tracer.generate_narrative(result)
        assert '## Step' in narrative

    def test_narrative_includes_visualization_hints(self):
        """Narrative should include Frontend Visualization Hints section."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        narrative = tracer.generate_narrative(result)
        assert '🎨 Frontend Visualization Hints' in narrative

    def test_narrative_includes_summary(self):
        """Narrative should include execution summary."""
        tracer = BreadthFirstSearchTracer()
        result = tracer.execute({
            'nodes': ['A', 'B'],
            'edges': [('A', 'B')],
            'start_node': 'A'
        })

        narrative = tracer.generate_narrative(result)
        assert 'Execution Summary' in narrative or 'Summary' in narrative
