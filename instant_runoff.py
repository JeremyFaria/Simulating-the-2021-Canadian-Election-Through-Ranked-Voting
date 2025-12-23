from redistribute_votes_int import redistribute_votes_integer

def run_instant_runoff(row, matrix, parties):
    """Simulating IRV for a single riding"""
    votes = row[parties].to_dict()
    eliminated = set()
    
    while True:
        total_votes = sum(votes.values())
        # Check for majority
        for party, count in votes.items():
            if count > total_votes / 2:
                return party
        
        # Find lowest party
        remaining = {k: v for k, v in votes.items() if k not in eliminated}
        if len(remaining) == 1:
            return next(iter(remaining))

        loser = min(remaining, key=remaining.get)
        loser_index = parties.index(loser)
        alpha = [matrix[loser_index][i] for i in range(len(parties)) if parties[i] not in eliminated and parties[i] != loser]

        # Normalizing alpha
        target_parties = [p for p in parties if p not in eliminated and p != loser]
        redistributed = redistribute_votes_integer(int(votes[loser]), alpha, target_parties)
        for p, v in redistributed.items():
            votes[p] += v
        
        votes[loser] = 0
        eliminated.add(loser)