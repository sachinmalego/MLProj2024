import numpy as np
from scipy.stats import pearsonr
from sklearn.metrics.pairwise import pairwise_distances

# Function to calculate spatial distance-based permutation
def spatial_permutation_test(pollution, traffic, coordinates, n_permutations=1000, max_distance=1.0):
    """
    Perform a spatial permutation test by shuffling traffic values with spatial constraints.
    
    Parameters:
        pollution (array): Array of pollution (PM2.5) values at sensor locations.
        traffic (array): Array of traffic volume values at sensor locations.
        coordinates (array): Array of coordinates (lat, lon) for sensor locations.
        n_permutations (int): Number of permutations to perform.
        max_distance (float): Maximum distance within which traffic values can be shuffled.
    
    Returns:
        observed_corr (float): The observed correlation between traffic and pollution.
        p_value (float): The p-value of the spatial permutation test.
    """
    
    # Compute the observed correlation
    print(len(traffic), len(pollution))
    observed_corr, _ = pearsonr(traffic, pollution)
    
    # Store permuted correlations
    permuted_corrs = []
    
    # Compute pairwise distances between sensor locations
    dist_matrix = pairwise_distances(coordinates, metric='euclidean')
    
    # Perform permutations with spatial constraints
    for _ in range(n_permutations):
        permuted_traffic = traffic.copy()
        
        # Shuffle traffic values while keeping spatial distance constraint
        for i in range(len(traffic)):
            # Find locations within a specified max_distance
            close_indices = np.where(dist_matrix[i] <= max_distance)[0]
            # Permute only traffic values of close locations
            permuted_traffic[close_indices] = np.random.permutation(traffic[close_indices])
        
        # Calculate the correlation of the permuted data
        permuted_corr, _ = pearsonr(permuted_traffic, pollution)
        permuted_corrs.append(permuted_corr)
    
    # Calculate p-value
    permuted_corrs = np.array(permuted_corrs)
    p_value = np.mean(np.abs(permuted_corrs) >= np.abs(observed_corr))
    
    return observed_corr, p_value


