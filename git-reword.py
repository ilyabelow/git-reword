#!/usr/bin/env python
import pygit2
import sys


class RewordMachine:
    def __init__(self, repo_path):
        """Open repo"""
        self.repo = pygit2.Repository(repo_path)

    def run(self, request):
        """Start rewording on current repo according to request"""
        self.mapping = self.normalize(request)
        self.to_find = len(self.mapping)

        # Start recursive descend
        new_last_commit = self.recursive_reword(
                self.repo.revparse_single('HEAD')
                )
        # TODO update all references to the line?
        self.repo.head.set_target(new_last_commit.hex)

    def recursive_reword(self, commit):
        """Tweak all commits in the line"""
        self.found(commit)
        new_parents = []

        if not self.found_all():
            if len(commit.parents) > 1:
                # Supporting branching would require a BFS here,
                # which sounds unnecessary?
                raise Exception("Support only commits in one row")
            if len(commit.parents) == 0:
                raise Exception("End of chain reached")
            # RECURSIVE DESCEND HERE!
            new_parents = [self.recursive_reword(commit.parents[0])]
        else:
            new_parents = commit.parents  # Might be several

        # Creating new commit
        new_commit = self.repo.create_commit(
                None,                           # do not update any refs
                commit.author,                  # OLD author
                commit.committer,               # OLD commiter
                self.get_reword(commit),        # NEW message
                commit.tree.hex,                # OLD tree
                [p.hex for p in new_parents])   # NEW parents

        # TODO delete old commit. I don't know yet how
        return self.repo.get(new_commit)

    def normalize(self, mapping):
        """Resolve all shortened refs into commit objects"""
        new_mapping = {}
        for key in mapping.keys():
            new_mapping[self.repo.revparse_single(key)] = mapping[key]
        return new_mapping

    def need_change(self, commit):
        return commit in self.mapping.keys()

    def get_reword(self, commit):
        """Get message to be set on a commit"""
        if self.need_change(commit):
            return self.mapping[commit]
        return commit.message

    def found(self, commit):
        """Record how much commits there is to be found"""
        if self.need_change(commit):
            self.to_find -= 1

    def found_all(self):
        return self.to_find == 0


def resolve_request():
    """Parse command line args"""
    # TODO file support
    return dict(zip(sys.argv[1::2], sys.argv[2::2]))

rwm = RewordMachine('.')
rwm.run(resolve_request())
