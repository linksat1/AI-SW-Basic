"""과제 필수 기능과 검수에서 발견한 오류의 회귀 테스트.

실행: python -B -m unittest discover -s tests -v
"""

import ast
from datetime import datetime, timedelta
from pathlib import Path
import random
import subprocess
import sys
import unittest
from unittest.mock import patch

from mini_git.cli import dispatch
from mini_git.commit import Commit, generate_commit_hash
from mini_git.repository import Repository
from mini_git.sorting import merge_sort
from mini_git.traversal import ancestors, shortest_path, topological_order


class MiniGitTests(unittest.TestCase):
    """CLI, 저장소 상태, 탐색, 정렬, 역색인의 외부 동작을 검증한다."""

    def setUp(self):
        self.repo = Repository()
        self.repo.init('Alice Kim')
        self.time = datetime(2026, 1, 1)

    def node(self, commit_hash, parents=(), author='Alice', day=0):
        return Commit(commit_hash, 'message', author,
                      self.time + timedelta(days=day), parents, 'main')

    def test_branch_commit_and_topological_log(self):
        root = self.repo.commit('Initial')
        self.repo.branch('feature')
        self.repo.switch('feature')
        feature = self.repo.commit('Feature')
        self.repo.switch('main')
        main = self.repo.commit('Main')
        self.assertEqual(root.parents, [])
        self.assertEqual(feature.parents, [root.hash])
        self.assertEqual(main.parents, [root.hash])
        self.assertEqual(self.repo.branches, {'main': main.hash, 'feature': feature.hash})
        self.assertEqual(self.repo.log()[0], root)
        self.assertEqual(self.repo.shortest_path(feature.hash, main.hash),
                         [feature.hash, root.hash, main.hash])

    def test_existing_branch_preserves_all_state(self):
        self.repo.commit('Root')
        self.repo.branch('feature')
        self.repo.commit('Main next')
        self.repo.switch('feature')
        before = dict(self.repo.branches)
        self.assertEqual(dispatch(self.repo, 'branch main'), 'Invalid args')
        self.assertEqual(dispatch(self.repo, 'branch feature'), 'Invalid args')
        self.assertEqual(self.repo.branches, before)
        self.assertEqual(self.repo.current_branch, 'feature')

    def test_repeated_keyword_returns_one_commit(self):
        commit = self.repo.commit('login login LOGIN')
        self.assertEqual(self.repo.search_keyword('LOGIN'), [commit])
        self.assertIn('Found 1 commit:', dispatch(self.repo, 'search login'))

    def test_phrase_order_contiguity_repetition_and_normalization(self):
        first = self.repo.commit('Add Login   Feature')
        self.repo.commit('feature login')
        self.repo.commit('login another feature')
        repeated = self.repo.commit('login login feature')
        self.assertEqual(self.repo.search_keyword(' LOGIN\tFEATURE '), [first, repeated])
        self.assertEqual(self.repo.search_keyword('login login'), [repeated])
        self.assertEqual(self.repo.search_keyword('login missing'), [])
        self.assertIn('Found 2 commits:', dispatch(self.repo, 'search "login feature"'))

    def test_search_does_not_iterate_all_commits(self):
        matching = self.repo.commit('Add login feature')
        self.repo.commit('Unrelated')

        class LookupOnly(dict):
            def __iter__(self):
                raise AssertionError('전체 커밋 순회 금지')

            def items(self):
                raise AssertionError('전체 커밋 순회 금지')

            def values(self):
                raise AssertionError('전체 커밋 순회 금지')

        self.repo.commits = LookupOnly(self.repo.commits)
        self.assertEqual(self.repo.search_keyword('login'), [matching])
        self.assertEqual(self.repo.search_keyword('login feature'), [matching])
        self.assertEqual(len(self.repo.search_author('Alice Kim')), 2)

    def test_author_with_spaces_and_init_resets_indexes(self):
        self.repo.commit('login login')
        self.assertIn('Found 1 commit:', dispatch(self.repo, 'SEARCH --author="Alice Kim"'))
        self.assertEqual(self.repo.search_author('alice kim'), [])
        dispatch(self.repo, 'init Bob')
        self.assertEqual(self.repo.commits, {})
        self.assertEqual(self.repo.branches, {'main': None})
        self.assertEqual(self.repo.search_keyword('login'), [])
        self.assertEqual(self.repo.search_keyword('login login'), [])
        self.assertEqual(self.repo.search_author('Alice Kim'), [])

    def test_standard_errors_and_empty_arguments(self):
        expected = {
            'switch missing': 'Unknown branch: missing',
            'ancestors missing': 'Unknown commit: missing',
            'path missing other': 'Unknown commit: missing',
            'log --sort-by=bad': 'Invalid args',
            'commit': 'Invalid args',
            'commit "unfinished': 'Invalid args',
            'init Alice Bob': 'Invalid args',
            'unknown': 'Invalid args',
        }
        for verb in ('init', 'branch', 'switch', 'commit', 'search'):
            expected[verb + ' "   "'] = 'Invalid args'
            expected[verb + ' ""'] = 'Invalid args'
        expected['search --author="   "'] = 'Invalid args'
        expected['search --author='] = 'Invalid args'
        for command, message in expected.items():
            with self.subTest(command=command):
                self.assertEqual(dispatch(self.repo, command), message)
        self.assertEqual(dispatch(Repository(), 'log'),
                         'Repository not initialized. Run INIT first.')

    def test_disconnected_and_identical_path(self):
        self.repo.branch('empty')
        first = self.repo.commit('First root')
        self.repo.switch('empty')
        second = self.repo.commit('Second root')
        self.assertEqual(dispatch(self.repo, f'path {first.hash} {second.hash}'), 'No path')
        self.assertEqual(self.repo.shortest_path(first.hash, first.hash), [first.hash])
        self.assertEqual(self.repo.ancestors(first.hash), [])

    def test_random_dags_against_independent_oracles(self):
        rng = random.Random(42)
        hashes = [f'{i:06x}' for i in range(8)]
        for case in range(50):
            graph = {h: self.node(h, [p for p in hashes[:i] if rng.random() < .3])
                     for i, h in enumerate(hashes)}
            order = topological_order(graph)
            self.assertEqual(set(order), set(hashes))
            position = {h: i for i, h in enumerate(order)}
            adjacency = {h: set() for h in hashes}
            for h, commit in graph.items():
                for parent in commit.parents:
                    self.assertLess(position[parent], position[h])
                    adjacency[h].add(parent)
                    adjacency[parent].add(h)
            for start in hashes:
                expected = set()
                pending = list(graph[start].parents)
                while pending:
                    h = pending.pop()
                    if h not in expected:
                        expected.add(h)
                        pending.extend(graph[h].parents)
                result = ancestors(graph, start)
                self.assertEqual(set(result), expected)
                self.assertEqual(len(result), len(expected))
            for start, end in ((hashes[0], hashes[-1]), (hashes[6], hashes[1])):
                candidates = []

                def walk(path):
                    if path[-1] == end:
                        candidates.append(path)
                        return
                    for neighbor in adjacency[path[-1]]:
                        if neighbor not in path:
                            walk(path + [neighbor])

                walk([start])
                best = min(candidates, key=lambda p: (len(p), '->'.join(p))) if candidates else None
                with self.subTest(case=case, start=start, end=end):
                    self.assertEqual(shortest_path(graph, start, end), best)

    def test_merge_ancestors_and_lexicographic_path(self):
        graph = {h: self.node(h, parents) for h, parents in (
            ('000000', []), ('000002', ['000000']), ('000001', ['000000']),
            ('000003', ['000002', '000001']))}
        self.assertEqual(shortest_path(graph, '000000', '000003'),
                         ['000000', '000001', '000003'])
        self.assertEqual(set(ancestors(graph, '000003')), {'000000', '000001', '000002'})

    def test_large_multi_parent_ancestors(self):
        graph = {f'{i:06x}': self.node(f'{i:06x}') for i in range(5000)}
        graph['ffffff'] = self.node('ffffff', list(graph))
        self.assertEqual(set(ancestors(graph, 'ffffff')), set(graph) - {'ffffff'})

    def test_sort_keys_and_stability(self):
        self.repo.commits = {f'{i:06x}': self.node(f'{i:06x}', author=name, day=day)
                             for i, (name, day) in enumerate(
                                 [('Charlie', 3), ('Alice', 2), ('Bob', 1), ('Alice', 0)])}
        self.assertEqual([c.hash for c in self.repo.log_sorted('author')],
                         ['000001', '000003', '000002', '000000'])
        self.assertEqual([c.hash for c in self.repo.log_sorted('date')],
                         ['000003', '000002', '000001', '000000'])
        rng = random.Random(7)
        for n in (0, 1, 2, 100, 1000):
            items = [(rng.randrange(8), i) for i in range(n)]
            original = list(items)
            result = merge_sort(items, key=lambda x: x[0])
            self.assertEqual(items, original)
            self.assertEqual(len(result), n)
            self.assertEqual(set(result), set(items))
            self.assertTrue(all(a[0] <= b[0] for a, b in zip(result, result[1:])))
            for key in range(8):
                self.assertEqual([x for x in result if x[0] == key],
                                 [x for x in items if x[0] == key])

    def test_hash_collision_retry(self):
        class Digest:
            def __init__(self, value):
                self.value = value

            def hexdigest(self):
                return self.value

        with patch('mini_git.commit.hashlib.sha1',
                   side_effect=[Digest('aaaaaa'), Digest('bbbbbb')]):
            self.assertEqual(generate_commit_hash({'aaaaaa'}, 'm', 'a', self.time, []), 'bbbbbb')

    def test_no_standard_sort_calls_or_graph_libraries(self):
        root = Path(__file__).resolve().parents[1]
        for path in [root / 'main.py', *root.joinpath('mini_git').glob('*.py')]:
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.Call):
                    self.assertFalse(isinstance(node.func, ast.Name) and node.func.id == 'sorted')
                    self.assertFalse(isinstance(node.func, ast.Attribute) and node.func.attr == 'sort')
                if isinstance(node, ast.Import):
                    self.assertTrue(all(a.name.split('.')[0] not in ('networkx', 'igraph') for a in node.names))

    def test_actual_entrypoint_repl_and_exit(self):
        root = Path(__file__).resolve().parents[1]
        for exit_command in ('ExIt', 'QuIt'):
            run = subprocess.run([sys.executable, '-B', 'main.py'], cwd=root,
                                 input='iNiT "Alice Kim"\nCommit "login login feature"\n'
                                       'SEARCH "login feature"\nlog\n' + exit_command + '\n',
                                 text=True, capture_output=True, timeout=10)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn('mini-git> ', run.stdout)
            self.assertIn('Found 1 commit:', run.stdout)
            self.assertIn('Alice Kim', run.stdout)


if __name__ == '__main__':
    unittest.main()
