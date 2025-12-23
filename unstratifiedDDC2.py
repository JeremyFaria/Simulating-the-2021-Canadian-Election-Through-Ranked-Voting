import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

# Party orderings
QUEBEC_PARTIES = ['Conservative Party of Canada', 'Liberal Party of Canada', 'New Democratic Party', 'Bloc Québécois', 'Green Party of Canada', 'People\'s Party of Canada']
CANADA_PARTIES = ['Conservative Party of Canada', 'Liberal Party of Canada', 'New Democratic Party', 'Green Party of Canada', 'People\'s Party of Canada']

# Create party index mappings once for efficiency
QUEBEC_PARTY_TO_IDX = {party: i for i, party in enumerate(QUEBEC_PARTIES)}
CANADA_PARTY_TO_IDX = {party: i for i, party in enumerate(CANADA_PARTIES)}

# Ranking matrices (alphas for Dirichlet)
Q_matrix = [
    [0, 0.118578397, 0.177867596, 0.654146341, 0.024703833, 0.024703833],
    [0.205117808, 0, 0.555024658, 0.1192, 0.096526027, 0.024131507],
    [0.146531532, 0.476227477, 0, 0.120810811, 0.219797297, 0.036632883],
    [0.418181818, 0.363636364, 0.181818182, 0, 0.018181818, 0.018181818],
    [0.08, 0.3, 0.45, 0.15, 0, 0.02],
    [0.7, 0.05, 0.04, 0.2, 0.01, 0]
]

C_matrix = [
    [0, 0.342857143, 0.514285714, 0.071428571, 0.071428571],
    [0.232876712, 0, 0.630136986, 0.109589041, 0.02739726],
    [0.166666667, 0.541666667, 0, 0.25, 0.041666667],
    [0.1, 0.35, 0.51, 0, 0.04],
    [0.82, 0.1, 0.05, 0.03, 0]
]

def redistribute_votes_integer(loser_votes, alpha, target_parties):
    """Redistribute votes using Dirichlet distribution"""
    proportions = np.random.dirichlet(alpha)
    raw_votes = proportions * loser_votes
    int_votes = np.floor(raw_votes).astype(int)
    remainder = loser_votes - int_votes.sum()

    # Assign remaining votes to parties
    remainders = raw_votes - int_votes
    for i in np.argsort(remainders)[::-1][:remainder]:
        int_votes[i] += 1

    return dict(zip(target_parties, int_votes))

def simulate_voter_preferences_batch(first_choice, matrix, parties, party_to_idx, num_voters, num_parties_ranked_dist):
    """Simulate voter preferences in batch for better performance"""
    if num_voters <= 0:
        return []
    
    # Get alpha values for the first choice party
    first_choice_idx = party_to_idx[first_choice]
    alpha = [matrix[first_choice_idx][i] for i in range(len(parties)) if parties[i] != first_choice]
    
    # Normalize alpha to sum to 1
    alpha_sum = sum(alpha)
    if alpha_sum > 0:
        alpha = [a / alpha_sum for a in alpha]
    else:
        # If all zeros, use uniform distribution
        alpha = [1.0 / (len(parties) - 1)] * (len(parties) - 1)
    
    # Generate number of parties ranked for each voter
    num_parties_ranked = np.random.choice([1, 2, 3, 4, 5], size=num_voters, p=[0.1, 0.2, 0.3, 0.25, 0.15])
    
    ballots = []
    for voter_num_parties in num_parties_ranked:
        preferences = [first_choice]
        remaining_parties = [p for p in parties if p != first_choice]
        current_alpha = alpha.copy()
        
        # Generate preferences using Dirichlet distribution
        for _ in range(min(voter_num_parties - 1, len(remaining_parties))):
            if len(remaining_parties) == 0:
                break
                
            # Sample from Dirichlet distribution
            proportions = np.random.dirichlet(current_alpha)
            
            # Ensure proportions sum to 1 and are valid
            proportions = np.maximum(proportions, 1e-10)  # Avoid zeros
            proportions = proportions / proportions.sum()  # Renormalize
            
            chosen_idx = np.random.choice(len(remaining_parties), p=proportions)
            chosen_party = remaining_parties[chosen_idx]
            
            preferences.append(chosen_party)
            remaining_parties.pop(chosen_idx)
            
            # Update alpha for remaining parties
            if len(remaining_parties) > 0:
                current_alpha.pop(chosen_idx)
                # Renormalize
                alpha_sum = sum(current_alpha)
                if alpha_sum > 0:
                    current_alpha = [a / alpha_sum for a in current_alpha]
                else:
                    current_alpha = [1.0 / len(remaining_parties)] * len(remaining_parties)
        
        ballots.append(preferences)
    
    return ballots

def create_pairwise_matrix_optimized(ballots, parties, party_to_idx):
    """Create pairwise comparison matrix from ballots - optimized version"""
    n_parties = len(parties)
    matrix = np.zeros((n_parties, n_parties))
    
    for ballot in ballots:
        ballot_len = len(ballot)
        for i in range(ballot_len):
            for j in range(i + 1, ballot_len):  # Only process each pair once
                idx1 = party_to_idx[ballot[i]]
                idx2 = party_to_idx[ballot[j]]
                matrix[idx1][idx2] += 1
    
    return matrix

def find_condorcet_winner_optimized(matrix, parties):
    """Find Condorcet winner from pairwise matrix - optimized with early termination"""
    n_parties = len(parties)
    
    for i in range(n_parties):
        is_winner = True
        for j in range(n_parties):
            if i != j and matrix[i][j] <= matrix[j][i]:
                is_winner = False
                break  # Early termination
        if is_winner:
            return parties[i]
    
    return None

def find_weakest_defeat_optimized(matrix, parties):
    """Find the weakest defeat in the pairwise matrix - optimized"""
    n_parties = len(parties)
    min_margin = float('inf')
    weakest_defeat = None
    
    # Only check upper triangle since we only store defeats in one direction
    for i in range(n_parties):
        for j in range(i + 1, n_parties):
            if matrix[i][j] > matrix[j][i]:
                margin = matrix[i][j] - matrix[j][i]
                if margin < min_margin:
                    min_margin = margin
                    weakest_defeat = (i, j)
            elif matrix[j][i] > matrix[i][j]:
                margin = matrix[j][i] - matrix[i][j]
                if margin < min_margin:
                    min_margin = margin
                    weakest_defeat = (j, i)
    
    return weakest_defeat

def run_ddc_optimized(ballots, parties, party_to_idx):
    """Run Defeat Dropping Condorcet algorithm - optimized version"""
    if not ballots:
        return parties[0]  # Fallback if no ballots
        
    matrix = create_pairwise_matrix_optimized(ballots, parties, party_to_idx)
    max_iterations = len(parties) * (len(parties) - 1) // 2  # Maximum possible defeats
    iterations = 0
    
    while iterations < max_iterations:
        # Check for Condorcet winner
        winner = find_condorcet_winner_optimized(matrix, parties)
        if winner:
            return winner
        
        # Find weakest defeat and drop it
        weakest_defeat = find_weakest_defeat_optimized(matrix, parties)
        if not weakest_defeat:
            break  # No more defeats to drop
            
        winner_idx, loser_idx = weakest_defeat
        matrix[winner_idx][loser_idx] = 0  # Drop the defeat
        iterations += 1
    
    # If we get here, no Condorcet winner found after dropping all defeats
    # Return the party with the most first-place votes as a fallback
    first_place_counts = defaultdict(int)
    for ballot in ballots:
        if ballot:
            first_place_counts[ballot[0]] += 1
    
    if first_place_counts:
        return max(first_place_counts, key=first_place_counts.get)
    
    return parties[0]  # Fallback to first party

def simulate_riding_ddc_optimized(row, matrix, parties, party_to_idx):
    """Simulate DDC for a single riding - optimized version using weighted sampling"""
    votes = row[parties].to_dict()
    
    print(f"    Processing riding with vote counts: {votes}")
    
    # Instead of generating millions of individual ballots, use weighted sampling
    # Sample a reasonable number of ballots that represent the vote distribution
    total_votes = sum(votes.values())
    sample_size = int(min(10000, total_votes))  # Sample at most 10k ballots
    
    # Calculate sampling weights for each party
    sampling_weights = [votes[party] / total_votes for party in parties]
    
    # Generate sampled ballots
    ballots = []
    for _ in range(sample_size):
        # Sample first choice based on vote shares
        first_choice = np.random.choice(parties, p=sampling_weights)
        
        # Generate preferences for this voter
        preferences = simulate_single_voter_preferences(first_choice, matrix, parties, party_to_idx)
        ballots.append(preferences)
    
    print(f"    Generated {len(ballots)} sample ballots from {total_votes} total votes")
    print(f"    Running DDC algorithm...")
    
    # Run DDC on the ballots
    winner = run_ddc_optimized(ballots, parties, party_to_idx)
    print(f"    DDC winner: {winner}")
    return winner

def simulate_single_voter_preferences(first_choice, matrix, parties, party_to_idx):
    """Simulate preferences for a single voter"""
    preferences = [first_choice]
    remaining_parties = [p for p in parties if p != first_choice]
    
    if len(remaining_parties) == 0:
        return preferences
    
    # Get alpha values for the first choice party
    first_choice_idx = party_to_idx[first_choice]
    alpha = [matrix[first_choice_idx][i] for i in range(len(parties)) if parties[i] != first_choice]
    
    # Normalize alpha to sum to 1
    alpha_sum = sum(alpha)
    if alpha_sum > 0:
        alpha = [a / alpha_sum for a in alpha]
    else:
        # If all zeros, use uniform distribution
        alpha = [1.0 / (len(parties) - 1)] * (len(parties) - 1)
    
    # Determine how many parties this voter ranks
    num_parties_ranked = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.2, 0.3, 0.25, 0.15])
    
    # Generate preferences using Dirichlet distribution
    for _ in range(min(num_parties_ranked - 1, len(remaining_parties))):
        if len(remaining_parties) == 0:
            break
            
        # Sample from Dirichlet distribution
        proportions = np.random.dirichlet(alpha)
        
        # Ensure proportions sum to 1 and are valid
        proportions = np.maximum(proportions, 1e-10)  # Avoid zeros
        proportions = proportions / proportions.sum()  # Renormalize
        
        chosen_idx = np.random.choice(len(remaining_parties), p=proportions)
        chosen_party = remaining_parties[chosen_idx]
        
        preferences.append(chosen_party)
        remaining_parties.pop(chosen_idx)
        
        # Update alpha for remaining parties
        if len(remaining_parties) > 0:
            alpha.pop(chosen_idx)
            # Renormalize
            alpha_sum = sum(alpha)
            if alpha_sum > 0:
                alpha = [a / alpha_sum for a in alpha]
            else:
                alpha = [1.0 / len(remaining_parties)] * len(remaining_parties)
    
    return preferences

def simulate_election_ddc(df, strat):
    """Simulate DDC election (stratified or unstratified) - optimized"""
    results = []
    total_ridings = len(df)
    print(f"Processing {total_ridings} ridings...")
    
    for i, row in df.iterrows():
        if i % 10 == 0:  # Progress indicator every 10 ridings
            print(f"  Processing riding {i+1}/{total_ridings}...")
            
        if strat == False:
            if row["GroupKey"].startswith("24"):
                winner = simulate_riding_ddc_optimized(row, Q_matrix, QUEBEC_PARTIES, QUEBEC_PARTY_TO_IDX)
            else:
                winner = simulate_riding_ddc_optimized(row, C_matrix, CANADA_PARTIES, CANADA_PARTY_TO_IDX)
        else:
            if row["Riding_number"].startswith("24"):
                winner = simulate_riding_ddc_optimized(row, Q_matrix, QUEBEC_PARTIES, QUEBEC_PARTY_TO_IDX)
            else:
                winner = simulate_riding_ddc_optimized(row, C_matrix, CANADA_PARTIES, CANADA_PARTY_TO_IDX)
        results.append(winner)
    
    print("  All ridings processed!")
    df['DDC_winner'] = results
    return df

def generate_histograms_from_lists(conservative, ndp, liberal, ppc, green, bloc) -> None:
    """Generate histograms for each party's seat distribution across simulations"""
    print("\n=== GENERATING HISTOGRAMS ===")
    
    parties = ["Conservative", "NDP", "Liberal", "PPC", "Green", "Bloc"]
    party_data = [conservative, ndp, liberal, ppc, green, bloc]
    colors = {
        "Conservative": "blue",
        "NDP": "orange", 
        "Liberal": "red",
        "PPC": "purple",
        "Green": "green",
        "Bloc": "cyan"
    }

    # Combined subplot
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('DDC Seat Distribution Histograms by Party', fontsize=16)
    
    for idx, (party, data) in enumerate(zip(parties, party_data)):
        if not data:
            continue

        mean_seats = sum(data) / len(data)
        std_dev = (sum((s - mean_seats) ** 2 for s in data) / len(data)) ** 0.5
        coeff_var = std_dev / mean_seats if mean_seats != 0 else 0
        
        row, col = divmod(idx, 3)
        ax = axes[row, col]

        bins = range(min(data), max(data) + 2) if max(data) > min(data) else [min(data) - 0.5, min(data) + 0.5]

        ax.hist(data, bins=bins, edgecolor='black', color=colors[party], alpha=0.7, align='left')
        ax.axvline(mean_seats, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_seats:.1f}')
        
        ax.set_xlabel(f'{party} Seats')
        ax.set_ylabel('Frequency')
        ax.set_title(f'{party} Seat Distribution\n(μ={mean_seats:.1f}, cv={coeff_var:.2f})')
        ax.legend()
        ax.grid(True, alpha=0.3)

        stats_text = f'Mean: {mean_seats:.1f}\ncoeff_var: {coeff_var:.2f}\nRange: {min(data)}–{max(data)}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.show()

    # Individual histograms
    print("\nGenerating individual party histograms...")
    for party, data in zip(parties, party_data):
        if not data:
            continue

        mean_seats = sum(data) / len(data)
        std_dev = (sum((s - mean_seats) ** 2 for s in data) / len(data)) ** 0.5
        coeff_var = std_dev / mean_seats if mean_seats != 0 else 0
        bins = range(min(data), max(data) + 2) if max(data) > min(data) else [min(data) - 0.5, min(data) + 0.5]

        plt.figure(figsize=(8, 6))
        plt.hist(data, bins=bins, edgecolor='black', color=colors[party], alpha=0.7, align='left')
        plt.axvline(mean_seats, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_seats:.1f}')
        
        plt.xlabel(f'{party} Seats')
        plt.ylabel('Frequency')
        plt.title(f'DDC Variance of {party} Seats\n(μ={mean_seats:.1f}, cv={coeff_var:.2f})')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

def main():
    """Main function to run DDC simulation"""
    print("Loading election data...")
    
    # Load and prepare data
    df = pd.read_csv("combined_voting_data_final.csv")
    df_header = df.rename(columns={
        'Electoral.District.Number.Numéro.de.circonscription': 'Riding_number', 
        'Electoral.District.Name.Nom.de.circonscription': 'Riding_name'
    })
    
    # Fix specific riding data
    df_header.loc[df_header['Riding_number'] == 24002, 'Conservative Party of Canada'] = 5339
    df_clean = df_header.fillna(0)
    df_clean['Riding_number'] = df_clean['Riding_number'].astype(str)
    
    # Create unstratified data
    df_inter = df_clean
    df_inter['GroupKey'] = df_inter['Riding_number'].str[:2]
    
    df_unstrat = (
        df_inter.groupby('GroupKey')
          .agg({col: 'sum' for col in df_inter.columns[2:8]}  
               | {'Riding_number': 'count'})                     
          .rename(columns={'Riding_number': 'Ridings'})         
          .reset_index()
    )
    
    print(f"Unstratified data shape: {df_unstrat.shape}")
    print("Running unstratified DDC simulation...")
    
    # Run unstratified DDC simulation
    lib_seats = []
    con_seats = []
    bloc_seats = []
    ndp_seats = []
    green_seats = []
    ppc_seats = []
    
    num_simulations = 15  # Reduced for faster testing
    
    for i in range(num_simulations):
        print(f"\n=== Starting simulation {i+1}/{num_simulations} ===")
        
        try:
            df_final = simulate_election_ddc(df_unstrat, False)
            result = df_final.groupby('DDC_winner', as_index=True)['Ridings'].sum()
            
            lib_seats.append(int(result.loc['Liberal Party of Canada']))
            con_seats.append(int(result.loc['Conservative Party of Canada']))
            
            if ('Bloc Québécois' in result.index):
                bloc_seats.append(int(result.loc['Bloc Québécois']))
            else:
                bloc_seats.append(0)

            if ('New Democratic Party' in result.index):
                ndp_seats.append(int(result.loc['New Democratic Party']))
            else:
                ndp_seats.append(0)

            if ('Green Party of Canada' in result.index):
                green_seats.append(int(result.loc['Green Party of Canada']))
            else:
                green_seats.append(0)
            ppc_seats.append(0)
            
            print(f"Simulation {i+1} completed successfully!")
            
        except Exception as e:
            print(f"Error in simulation {i+1}: {e}")
            import traceback
            traceback.print_exc()
            break
    
    print("Simulation complete! Generating results...")
    
    # Print summary statistics
    print("\n=== DDC SIMULATION RESULTS ===")
    print(f"Number of simulations: {len(lib_seats)}")
    if lib_seats:
        print(f"Liberal mean seats: {sum(lib_seats)/len(lib_seats):.1f}")
        print(f"Conservative mean seats: {sum(con_seats)/len(con_seats):.1f}")
        print(f"NDP mean seats: {sum(ndp_seats)/len(ndp_seats):.1f}")
        print(f"Bloc mean seats: {sum(bloc_seats)/len(bloc_seats):.1f}")
        print(f"Green mean seats: {sum(green_seats)/len(green_seats):.1f}")
        print(f"PPC mean seats: {sum(ppc_seats)/len(ppc_seats):.1f}")
        
        # Generate histograms
        generate_histograms_from_lists(con_seats, ndp_seats, lib_seats, ppc_seats, green_seats, bloc_seats)
    else:
        print("No simulations completed successfully.")

if __name__ == "__main__":
    main()
