import numpy as np

def redistribute_votes_integer(loser_votes, alpha, target_parties):
    proportions = np.random.dirichlet(alpha)
    raw_votes = proportions * loser_votes
    int_votes = np.floor(raw_votes).astype(int)
    remainder = loser_votes - int_votes.sum()

    # Assign remaining votes to parties
    remainders = raw_votes - int_votes
    for i in np.argsort(remainders)[::-1][:remainder]:
        int_votes[i] += 1

    return dict(zip(target_parties, int_votes))