import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import random
from collections import defaultdict
import matplotlib.pyplot as plt

class DefeatDroppingCondorcet:
    """Defeat Dropping Condorcet (DDC) voting method implementation."""
    
    def __init__(self, parties: List[str]):
        self.parties = parties
        self.n_parties = len(parties)
        
    def create_pairwise_matrix(self, ballots: List[List[str]]) -> np.ndarray:
        """Create pairwise comparison matrix from ranked ballots."""
        matrix = np.zeros((self.n_parties, self.n_parties))
        
        for ballot in ballots:
            ballot_len = len(ballot)
            for i in range(ballot_len):
                for j in range(ballot_len):  # Process all pairs (less efficient)
                    if i != j:  # Don't compare party with itself
                        party1, party2 = ballot[i], ballot[j]
                        idx1 = self.parties.index(party1)
                        idx2 = self.parties.index(party2)
                        matrix[idx1][idx2] += 1
                        
        return matrix
    
    def find_weakest_defeat(self, matrix: np.ndarray) -> Optional[Tuple[int, int, float]]:
        """Find the weakest defeat in the pairwise matrix."""
        defeats = []
        
        for i in range(self.n_parties):
            for j in range(self.n_parties):
                if i != j and matrix[i][j] > matrix[j][i]:
                    margin = matrix[i][j] - matrix[j][i]
                    defeats.append((i, j, margin))
        
        if not defeats:
            return None
            
        # Return the defeat with the smallest margin
        return min(defeats, key=lambda x: x[2])
    
    def find_condorcet_winner(self, matrix: np.ndarray) -> Optional[int]:
        """Find Condorcet winner in the current matrix."""
        for i in range(self.n_parties):
            is_condorcet_winner = True
            for j in range(self.n_parties):
                if i != j and matrix[i][j] <= matrix[j][i]:
                    is_condorcet_winner = False
                    break
            if is_condorcet_winner:
                return i
        return None
    
    def run_ddc(self, ballots: List[List[str]]) -> str:
        """Run the Defeat Dropping Condorcet method."""
        matrix = self.create_pairwise_matrix(ballots)
        
        while True:
            # Check for Condorcet winner
            condorcet_winner = self.find_condorcet_winner(matrix)
            if condorcet_winner is not None:
                return self.parties[condorcet_winner]
            
            # Find and drop weakest defeat
            weakest_defeat = self.find_weakest_defeat(matrix)
            if weakest_defeat is None:
                # No more defeats to drop, return party with most first preferences
                first_prefs = defaultdict(int)
                for ballot in ballots:
                    if ballot:
                        first_prefs[ballot[0]] += 1
                return max(first_prefs.items(), key=lambda x: x[1])[0]
            
            winner_idx, loser_idx, margin = weakest_defeat
            # Drop the defeat by setting both values to 0
            matrix[winner_idx][loser_idx] = 0
            matrix[loser_idx][winner_idx] = 0


class VoterSimulator:
    """Simulates voters based on IPSOS data and voting patterns."""
    
    def __init__(self):
        # IPSOS data: certainty levels and corresponding number of parties ranked
        self.certainty_levels = {
            "absolutely_certain": 0.46,    # 46% rank 1 party
            "fairly_certain": 0.39,        # 39% rank 2 parties  
            "not_very_certain": 0.11,      # 11% rank 3 parties
            "not_at_all_certain": 0.04     # 4% rank 4 parties
        }
        
        # Dirichlet parameters for uncertainty modeling
        self.dirichlet_params = {
            "absolutely_certain": 10.0,    # Very certain preferences
            "fairly_certain": 5.0,         # Moderately certain preferences
            "not_very_certain": 2.0,       # Less certain preferences
            "not_at_all_certain": 1.0      # Very uncertain preferences
        }
        
        self.parties = ["Conservative", "NDP", "Liberal", "PPC", "Green", "Bloc"]
        
        # Preference model based on ideological spectrum
        self.preference_model = {
            "Conservative": ["PPC", "Liberal", "NDP", "Green", "Bloc"],
            "NDP": ["Green", "Liberal", "Conservative", "PPC", "Bloc"],
            "Liberal": ["NDP", "Green", "Conservative", "PPC", "Bloc"],
            "PPC": ["Conservative", "Liberal", "NDP", "Green", "Bloc"],
            "Green": ["NDP", "Liberal", "Conservative", "PPC", "Bloc"],
            "Bloc": ["Liberal", "NDP", "Green", "Conservative", "PPC"]
        }
        
    def simulate_voter_preferences(self, first_choice: str, num_rankings: int, certainty_level: str = "fairly_certain") -> List[str]:
        """Simulate additional preferences for a voter based on their first choice using Dirichlet distribution."""
        if num_rankings == 1:
            return [first_choice]
        
        # Get preference order for this first choice
        preference_order = self.preference_model.get(first_choice, self.parties)
        
        # Get remaining parties (excluding first choice)
        remaining_parties = [p for p in preference_order if p != first_choice]
        
        if len(remaining_parties) == 0:
            return [first_choice]
        
        # Use Dirichlet distribution to model uncertainty in preferences
        alpha = self.dirichlet_params.get(certainty_level, 2.0)
        
        # Create alpha parameters for Dirichlet distribution
        dirichlet_alphas = []
        for party in remaining_parties:
            try:
                position = preference_order.index(party)
                # Inverse relationship: closer position = higher alpha
                dirichlet_alpha = alpha * (1.0 / (position + 1))
                dirichlet_alphas.append(dirichlet_alpha)
            except ValueError:
                dirichlet_alphas.append(alpha * 0.1)  # Default low preference
        
        # Sample from Dirichlet distribution
        if len(dirichlet_alphas) > 0:
            proportions = np.random.dirichlet(dirichlet_alphas)
            
            # Sort remaining parties by their sampled proportions (highest first)
            party_proportions = list(zip(remaining_parties, proportions))
            party_proportions.sort(key=lambda x: x[1], reverse=True)
            
            # Take the top (num_rankings - 1) parties
            additional_choices = [party for party, _ in party_proportions[:num_rankings - 1]]
        else:
            additional_choices = preference_order[:num_rankings - 1]
        
        return [first_choice] + additional_choices
    
    def simulate_riding_election(self, riding_data: Dict[str, int], num_voters: int) -> List[List[str]]:
        """Simulate an election for a single riding."""
        # Calculate vote shares for the 6 major parties
        total_votes = sum(riding_data.get(party, 0) for party in self.parties)
        
        if total_votes == 0:
            vote_shares = {party: 1.0 / len(self.parties) for party in self.parties}
        else:
            vote_shares = {party: riding_data.get(party, 0) / total_votes for party in self.parties}
        
        ballots = []
        
        for i in range(num_voters):
            # Determine number of rankings based on IPSOS data
            rand = random.random()
            num_rankings = 1  # default
            certainty_level = "fairly_certain"  # default
            
            cumulative = 0
            for certainty, prob in self.certainty_levels.items():
                cumulative += prob
                if rand <= cumulative:
                    certainty_level = certainty
                    # Map certainty level to number of rankings
                    if certainty == "absolutely_certain":
                        num_rankings = 1
                    elif certainty == "fairly_certain":
                        num_rankings = 2
                    elif certainty == "not_very_certain":
                        num_rankings = 3
                    elif certainty == "not_at_all_certain":
                        num_rankings = 4
                    break
            
            # Select first choice based on vote shares
            rand_choice = random.random()
            cumulative_share = 0
            first_choice = self.parties[0]  # default
            
            for party in self.parties:
                cumulative_share += vote_shares[party]
                if rand_choice <= cumulative_share:
                    first_choice = party
                    break
            
            # Generate complete ballot with Dirichlet uncertainty
            ballot = self.simulate_voter_preferences(first_choice, num_rankings, certainty_level)
            ballots.append(ballot)
        
        return ballots


def run_ddc(row, parties, voter_sample_size=None):
    """Run DDC for a single riding."""
    riding_data = row[parties].to_dict()
    
    total_votes = int(sum(riding_data.values()))
    if total_votes == 0:
        total_votes = 10000  # Default if no votes
    
    if voter_sample_size is not None:
        total_votes = min(total_votes, voter_sample_size)
    
    ddc = DefeatDroppingCondorcet(parties)
    simulator = VoterSimulator()
    
    ballots = simulator.simulate_riding_election(riding_data, total_votes)
    winner = ddc.run_ddc(ballots)
    
    return winner


def load_election_data(csv_file: str) -> pd.DataFrame:
    """Load election data from CSV file."""
    df = pd.read_csv(csv_file)
    
    # Map column names to party names
    column_mapping = {
        'Conservative Party of Canada': 'Conservative',
        'New Democratic Party': 'NDP', 
        'Liberal Party of Canada': 'Liberal',
        "People's Party of Canada": 'PPC',
        'Green Party of Canada': 'Green',
        'Bloc Québécois': 'Bloc'
    }
    
    df = df.rename(columns=column_mapping)
    
    # Handle NA values by replacing with 0
    party_columns = ['Conservative', 'NDP', 'Liberal', 'PPC', 'Green', 'Bloc']
    for col in party_columns:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    
    return df


def simulate_election_with_ddc(csv_file: str, num_simulations: int = 100, voter_sample_size: int = 1000) -> Dict:
    """Simulate elections using DDC method across all ridings."""
    df = load_election_data(csv_file)
    
    parties = ["Conservative", "NDP", "Liberal", "PPC", "Green", "Bloc"]
    ddc = DefeatDroppingCondorcet(parties)
    simulator = VoterSimulator()
    
    results = {
        'riding_results': {},
        'overall_winners': [],
        'party_seats': defaultdict(int),
        'party_seats_per_simulation': [],
        'original_winners': [],
        'changes': []
    }
    
    # Get original winners (FPTP)
    for _, riding in df.iterrows():
        riding_data = {
            'Conservative': riding.get('Conservative', 0),
            'NDP': riding.get('NDP', 0), 
            'Liberal': riding.get('Liberal', 0),
            'PPC': riding.get('PPC', 0),
            'Green': riding.get('Green', 0),
            'Bloc': riding.get('Bloc', 0)
        }
        original_winner = max(riding_data.items(), key=lambda x: x[1])[0]
        results['original_winners'].append(original_winner)
    
    for sim in range(num_simulations):
        print(f"Running simulation {sim + 1}/{num_simulations}")
        
        sim_winners = []
        
        for idx, riding in df.iterrows():
            riding_data = {
                'Conservative': riding.get('Conservative', 0),
                'NDP': riding.get('NDP', 0), 
                'Liberal': riding.get('Liberal', 0),
                'PPC': riding.get('PPC', 0),
                'Green': riding.get('Green', 0),
                'Bloc': riding.get('Bloc', 0)
            }
            
            num_voters = min(riding.get('Total.Votes.Total.des.votes', 10000), voter_sample_size)
            
            ballots = simulator.simulate_riding_election(riding_data, num_voters)
            winner = ddc.run_ddc(ballots)
            sim_winners.append(winner)
            
            # Store results for first simulation
            if sim == 0:
                results['riding_results'][riding['Electoral.District.Name.Nom.de.circonscription']] = {
                    'winner': winner,
                    'original_winner': results['original_winners'][idx],
                    'ballots': ballots
                }
        
        # Count seats by party for this simulation
        sim_seats = defaultdict(int)
        for winner in sim_winners:
            sim_seats[winner] += 1
            results['party_seats'][winner] += 1
        
        results['party_seats_per_simulation'].append(dict(sim_seats))
        results['overall_winners'].append(sim_winners)
    
    return results


def analyze_results(results: Dict) -> None:
    """Analyze and print simulation results."""
    print("\n=== DDC ELECTION SIMULATION RESULTS (UNOPTIMIZED) ===\n")
    
    # Overall seat distribution
    print("Average Seat Distribution:")
    total_sims = len(results['overall_winners'])
    for party, seats in results['party_seats'].items():
        avg_seats = seats / total_sims
        print(f"{party}: {avg_seats:.1f} seats")
    
    print(f"\nTotal simulations: {total_sims}")
    
    # Calculate and display variance for each party
    print("\n=== VARIANCE ANALYSIS ===")
    parties = ["Conservative", "NDP", "Liberal", "PPC", "Green", "Bloc"]
    
    # Summary table for variance
    print("\nVariance Summary Table:")
    print(f"{'Party':<12} {'Mean':<6} {'Std Dev':<8} {'Range':<12} {'CV (%)':<8}")
    print("-" * 50)
    
    for party in parties:
        party_seats = [sim_seats.get(party, 0) for sim_seats in results['party_seats_per_simulation']]
        
        if party_seats:
            mean_seats = sum(party_seats) / len(party_seats)
            variance = sum((seats - mean_seats) ** 2 for seats in party_seats) / len(party_seats)
            std_dev = variance ** 0.5
            cv_percent = (std_dev / mean_seats * 100) if mean_seats > 0 else 0
            
            print(f"{party:<12} {mean_seats:<6.1f} {std_dev:<8.2f} {min(party_seats):<2}-{max(party_seats):<9} {cv_percent:<8.1f}")
            
            # Detailed breakdown for each party
            print(f"\n{party} Details:")
            print(f"  Mean seats: {mean_seats:.1f}")
            print(f"  Variance: {variance:.2f}")
            print(f"  Standard deviation: {std_dev:.2f}")
            print(f"  Coefficient of variation: {cv_percent:.1f}%")
            print(f"  Range: {min(party_seats)} - {max(party_seats)} seats")
            print(f"  Seat counts per simulation: {party_seats}")
    
    # Show changes from FPTP to DDC
    print("\nChanges from FPTP to DDC (First Simulation):")
    changes = 0
    for riding_name, riding_data in results['riding_results'].items():
        if riding_data['winner'] != riding_data['original_winner']:
            print(f"{riding_name}: {riding_data['original_winner']} -> {riding_data['winner']}")
            changes += 1
    
    print(f"\nTotal riding changes: {changes} out of {len(results['riding_results'])}")
    
    # Show some example riding results
    print("\nExample Riding Results (First Simulation):")
    for riding_name, riding_data in list(results['riding_results'].items())[:5]:
        print(f"{riding_name}: {riding_data['winner']} (was {riding_data['original_winner']})")


def generate_histograms(results: Dict, save_plots: bool = True) -> None:
    """Generate histograms for each party's seat distribution across simulations."""
    print("\n=== GENERATING HISTOGRAMS (UNOPTIMIZED) ===")
    
    parties = ["Conservative", "NDP", "Liberal", "PPC", "Green", "Bloc"]
    colors = {
        "Conservative": "blue",
        "NDP": "orange", 
        "Liberal": "red",
        "PPC": "purple",
        "Green": "green",
        "Bloc": "cyan"
    }
    
    # Create two separate histograms
    # 1. All parties including PPC and Green
    plt.figure(figsize=(12, 8))
    
    # Find the overall range for consistent binning (all parties)
    all_seats = []
    for party in parties:
        party_seats = [sim_seats.get(party, 0) for sim_seats in results['party_seats_per_simulation']]
        all_seats.extend(party_seats)
    
    if all_seats:
        min_seats = min(all_seats)
        max_seats = max(all_seats)
        bins = np.linspace(min_seats - 0.5, max_seats + 0.5, max_seats - min_seats + 2)
    else:
        bins = np.linspace(0, 10, 11)  # Default bins if no data
    
    # Plot histograms for all parties on the same chart
    for party in parties:
        party_seats = [sim_seats.get(party, 0) for sim_seats in results['party_seats_per_simulation']]
        
        if party_seats:
            # Calculate statistics
            mean_seats = sum(party_seats) / len(party_seats)
            std_dev = (sum((seats - mean_seats) ** 2 for seats in party_seats) / len(party_seats)) ** 0.5
            
            # Create histogram with transparency
            plt.hist(party_seats, bins=bins, alpha=0.6, label=f'{party} (μ={mean_seats:.1f}, σ={std_dev:.2f})', 
                    color=colors[party], edgecolor='black', linewidth=0.5)
    
    # Add labels and title
    plt.xlabel('Number of Seats')
    plt.ylabel('Frequency')
    plt.title('Seat Distribution Histograms - All Parties (Unoptimized)')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    
    if save_plots:
        plt.savefig('ddc_seat_distributions_unoptimized.png', dpi=300, bbox_inches='tight')
        print("All parties histogram saved as 'ddc_seat_distributions_unoptimized.png'")
    
    plt.show()
    
    # 2. Major parties only (excluding PPC and Green)
    major_parties = ["Conservative", "NDP", "Liberal", "Bloc"]
    plt.figure(figsize=(12, 8))
    
    # Find the range for major parties only
    major_seats = []
    for party in major_parties:
        party_seats = [sim_seats.get(party, 0) for sim_seats in results['party_seats_per_simulation']]
        major_seats.extend(party_seats)
    
    if major_seats:
        min_seats = min(major_seats)
        max_seats = max(major_seats)
        bins = np.linspace(min_seats - 0.5, max_seats + 0.5, max_seats - min_seats + 2)
    else:
        bins = np.linspace(0, 10, 11)  # Default bins if no data
    
    # Plot histograms for major parties only
    for party in major_parties:
        party_seats = [sim_seats.get(party, 0) for sim_seats in results['party_seats_per_simulation']]
        
        if party_seats:
            # Calculate statistics
            mean_seats = sum(party_seats) / len(party_seats)
            std_dev = (sum((seats - mean_seats) ** 2 for seats in party_seats) / len(party_seats)) ** 0.5
            
            # Create histogram with transparency
            plt.hist(party_seats, bins=bins, alpha=0.6, label=f'{party} (μ={mean_seats:.1f}, σ={std_dev:.2f})', 
                    color=colors[party], edgecolor='black', linewidth=0.5)
    
    # Add labels and title
    plt.xlabel('Number of Seats')
    plt.ylabel('Frequency')
    plt.title('Seat Distribution Histograms - Major Parties Only (Unoptimized)')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    
    if save_plots:
        plt.savefig('ddc_seat_distributions_major_parties_unoptimized.png', dpi=300, bbox_inches='tight')
        print("Major parties histogram saved as 'ddc_seat_distributions_major_parties_unoptimized.png'")
    
    plt.show()
    
    # Create individual histograms for each party
    print("\nGenerating individual party histograms...")
    for party in parties:
        party_seats = [sim_seats.get(party, 0) for sim_seats in results['party_seats_per_simulation']]
        
        if party_seats:
            plt.figure(figsize=(8, 6))
            
            if max(party_seats) > min(party_seats):
                bins = range(min(party_seats), max(party_seats) + 2)
            else:
                bins = [min(party_seats) - 0.5, min(party_seats) + 0.5]
            
            plt.hist(party_seats, bins=bins, edgecolor='black', color=colors[party], 
                    alpha=0.7, align='left')
            
            mean_seats = sum(party_seats) / len(party_seats)
            std_dev = (sum((seats - mean_seats) ** 2 for seats in party_seats) / len(party_seats)) ** 0.5
            
            plt.axvline(mean_seats, color='red', linestyle='--', linewidth=2, 
                       label=f'Mean: {mean_seats:.1f}')
            
            plt.xlabel(f'{party} Seats')
            plt.ylabel('Frequency')
            plt.title(f'Variance of {party} Seats (Unoptimized)\n(μ={mean_seats:.1f}, σ={std_dev:.2f})')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            if save_plots:
                plt.savefig(f'{party.lower()}_seat_distribution_unoptimized.png', dpi=300, bbox_inches='tight')
                print(f"Saved {party} histogram as '{party.lower()}_seat_distribution_unoptimized.png'")
            
            plt.show()


if __name__ == "__main__":
    # Redirect output to file
    import sys
    original_stdout = sys.stdout
    
    with open('ddc_unoptimized_output.txt', 'w') as f:
        sys.stdout = f
        
        # Run simulation with unoptimized settings
        csv_file = "combined_voting_data_final.csv"
        results = simulate_election_with_ddc(csv_file, num_simulations=100, voter_sample_size=1000)
        
        # Analyze results
        analyze_results(results)
        
        # Generate histograms
        generate_histograms(results, save_plots=True)
    
    # Restore stdout
    sys.stdout = original_stdout
    print("Unoptimized DDC simulation completed. Results saved to 'ddc_unoptimized_output.txt'") 