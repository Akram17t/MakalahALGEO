"""
Advanced Drainage Network Analysis with Hydraulic Integration
==============================================================
Implementasi analisis jaringan drainase dengan integrasi:
1. Spectral Analysis (eigenvalue/eigenvector)
2. Power Iteration Method (eigenvalue centrality)
3. Spectral Radius Analysis (stabilitas jaringan)
4. Hydraulic Flow Modeling (elevation, capacity, rainfall, sediment)
5. Multi-factor Vulnerability Assessment

Formula lengkap:
Vul(i) = f(spectral_centrality, degree_centrality, hydraulic_factors)

Reference: BAB 2 Theory - Graf Berarah, Eigenvalue Centrality, Spectral Radius
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, List

class HydraulicDrainageAnalyzer:
    def __init__(self, nodes_file: str, edges_file: str):
        """
        Initialize analyzer dengan data nodes dan edges
        """
        self.nodes_file = nodes_file
        self.edges_file = edges_file
        
        # Data structures
        self.nodes = None
        self.edges = None
        self.adj_matrix = None
        self.degree_matrix = None
        self.laplacian = None
        
        # Spectral properties
        self.eigenvalues = None
        self.eigenvectors = None
        self.spectral_radius = None
        self.algebraic_connectivity = None
        
        # Centrality measures
        self.eigenvalue_centrality = None
        self.degree_centrality = None
        
        # Hydraulic factors
        self.hydraulic_vulnerability = None
        
        # Combined vulnerability
        self.vulnerability_scores = None
        
        print("="*70)
        print("ADVANCED DRAINAGE NETWORK ANALYZER")
        print("Spectral Analysis + Hydraulic Integration")
        print("="*70)
    
    def load_data(self):
        """Load nodes and edges data"""
        print("\n[1] Loading data...")
        
        self.nodes = pd.read_csv(self.nodes_file)
        self.edges = pd.read_csv(self.edges_file)
        
        n_nodes = len(self.nodes)
        n_edges = len(self.edges)
        
        print(f"  ✓ Loaded {n_nodes} nodes")
        print(f"  ✓ Loaded {n_edges} edges")
        print(f"  ✓ Hydraulic parameters detected:")
        print(f"    - Elevation: {self.nodes['elevation'].min():.1f} - {self.nodes['elevation'].max():.1f} m")
        print(f"    - Flow capacity: {self.nodes['flow_capacity'].min():.1f} - {self.nodes['flow_capacity'].max():.1f} m³/s")
        print(f"    - Rainfall: {self.nodes['rainfall_intensity'].min():.1f} - {self.nodes['rainfall_intensity'].max():.1f} mm/h")
        print(f"    - Sediment risk: {self.nodes['sediment_risk'].min():.3f} - {self.nodes['sediment_risk'].max():.3f}")
    
    def construct_matrices(self):
        """
        Construct adjacency, degree, and Laplacian matrices
        Use symmetric adjacency matrix (undirected graph treatment)
        """
        print("\n[2] Constructing graph matrices...")
        
        n = len(self.nodes)
        self.adj_matrix = np.zeros((n, n))
        
        # Build symmetric adjacency matrix
        for _, edge in self.edges.iterrows():
            src = int(edge['source']) - 1
            tgt = int(edge['target']) - 1
            
            # Symmetric: A[i,j] = A[j,i] = 1
            self.adj_matrix[src, tgt] = 1
            self.adj_matrix[tgt, src] = 1
        
        # Degree matrix
        degrees = np.sum(self.adj_matrix, axis=1)
        self.degree_matrix = np.diag(degrees)
        
        # Laplacian matrix: L = D - A
        self.laplacian = self.degree_matrix - self.adj_matrix
        
        avg_degree = np.mean(degrees)
        max_degree = np.max(degrees)
        min_degree = np.min(degrees)
        
        print(f"  ✓ Adjacency matrix: {n}×{n} (symmetric)")
        print(f"  ✓ Degree statistics:")
        print(f"    - Average degree: {avg_degree:.2f}")
        print(f"    - Max degree: {int(max_degree)}")
        print(f"    - Min degree: {int(min_degree)}")
    
    def spectral_analysis(self):
        """
        Perform eigenvalue decomposition on Laplacian matrix
        Compute algebraic connectivity (λ₂) and spectral properties
        """
        print("\n[3] Spectral Analysis (Eigenvalue Decomposition)...")
        
        # Eigenvalue decomposition (symmetric matrix)
        eigenvalues, eigenvectors = np.linalg.eigh(self.laplacian)
        
        # Sort by eigenvalue (ascending)
        idx = np.argsort(eigenvalues)
        self.eigenvalues = eigenvalues[idx]
        self.eigenvectors = eigenvectors[:, idx]
        
        # Algebraic connectivity (second smallest eigenvalue)
        self.algebraic_connectivity = self.eigenvalues[1]
        
        print(f"  ✓ Eigenvalue range: [{self.eigenvalues.min():.6f}, {self.eigenvalues.max():.6f}]")
        print(f"  ✓ Algebraic connectivity (λ₂): {self.algebraic_connectivity:.6f}")
        
        if self.algebraic_connectivity < 0.1:
            print(f"    ⚠ λ₂ < 0.1 → Network sangat fragile/rentan terputus")
        elif self.algebraic_connectivity < 0.5:
            print(f"    ⚠ λ₂ < 0.5 → Network cukup rentan")
        else:
            print(f"    ✓ λ₂ ≥ 0.5 → Network relatif robust")
    
    def compute_spectral_radius(self):
        """
        Compute spectral radius ρ(A) = max|λᵢ(A)|
        Spectral radius indicates network stability and connectivity spread
        """
        print("\n[4] Computing Spectral Radius ρ(A)...")
        
        # Eigenvalues of adjacency matrix (for spectral radius)
        adj_eigenvalues = np.linalg.eigvalsh(self.adj_matrix)
        self.spectral_radius = np.max(np.abs(adj_eigenvalues))
        
        print(f"  ✓ Spectral radius ρ(A): {self.spectral_radius:.6f}")
        print(f"  ✓ Interpretation:")
        
        n = len(self.nodes)
        avg_degree = np.mean(np.sum(self.adj_matrix, axis=1))
        
        if self.spectral_radius > avg_degree * 1.5:
            print(f"    → High spectral radius: dominasi hub nodes (star-like topology)")
        elif self.spectral_radius > avg_degree * 1.2:
            print(f"    → Moderate: beberapa hub nodes signifikan")
        else:
            print(f"    → Low: distribusi koneksi merata (mesh-like topology)")
    
    def power_iteration_centrality(self, max_iter: int = 100, tol: float = 1e-6):
        """
        Compute eigenvalue centrality using power iteration method
        Iterative method untuk mencari eigenvector dengan eigenvalue terbesar
        
        Power iteration formula:
        x_{k+1} = A·x_k / ||A·x_k||
        
        Converges to dominant eigenvector (highest eigenvalue)
        """
        print("\n[5] Power Iteration Method (Eigenvalue Centrality)...")
        
        n = len(self.nodes)
        
        # Initial random vector
        x = np.random.rand(n)
        x = x / np.linalg.norm(x)
        
        for iteration in range(max_iter):
            # Power iteration step
            x_new = self.adj_matrix @ x
            x_new_norm = np.linalg.norm(x_new)
            
            if x_new_norm < 1e-10:
                print(f"    ⚠ Warning: vector norm too small, using degree centrality fallback")
                x_new = np.sum(self.adj_matrix, axis=1)
                x_new = x_new / np.linalg.norm(x_new)
                break
            
            x_new = x_new / x_new_norm
            
            # Check convergence
            if np.linalg.norm(x_new - x) < tol:
                print(f"    ✓ Converged in {iteration+1} iterations")
                break
            
            x = x_new
        else:
            print(f"    ✓ Max iterations reached ({max_iter})")
        
        self.eigenvalue_centrality = np.abs(x)
        
        # Normalize to [0, 1]
        self.eigenvalue_centrality = (self.eigenvalue_centrality - self.eigenvalue_centrality.min())
        if self.eigenvalue_centrality.max() > 0:
            self.eigenvalue_centrality = self.eigenvalue_centrality / self.eigenvalue_centrality.max()
        
        print(f"  ✓ Eigenvalue centrality computed")
        print(f"    Range: [{self.eigenvalue_centrality.min():.4f}, {self.eigenvalue_centrality.max():.4f}]")
    
    def compute_degree_centrality(self):
        """
        Compute normalized degree centrality
        deg_centrality(i) = degree(i) / (n-1)
        """
        print("\n[6] Computing Degree Centrality...")
        
        degrees = np.sum(self.adj_matrix, axis=1)
        n = len(self.nodes)
        
        self.degree_centrality = degrees / (n - 1)
        
        print(f"  ✓ Degree centrality computed")
        print(f"    Range: [{self.degree_centrality.min():.4f}, {self.degree_centrality.max():.4f}]")
    
    def hydraulic_flow_analysis(self):
        """
        Analyze hydraulic vulnerability berdasarkan:
        1. Elevation (topography) - lower elevation = higher flood risk
        2. Flow capacity vs rainfall intensity
        3. Sediment risk - blockage probability
        4. Channel width - flow restriction
        5. Hydraulic load - capacity utilization
        
        Formula:
        H_vul(i) = w₁·elevation_risk + w₂·capacity_risk + w₃·sediment_risk + w₄·load_risk
        """
        print("\n[7] Hydraulic Flow Analysis...")
        
        # 1. Elevation risk (lower = higher risk)
        elevation = self.nodes['elevation'].values
        elevation_risk = 1 - (elevation - elevation.min()) / (elevation.max() - elevation.min())
        
        # 2. Capacity risk (rainfall/capacity ratio)
        rainfall = self.nodes['rainfall_intensity'].values
        capacity = self.nodes['flow_capacity'].values
        capacity_risk = rainfall / (capacity * 10)  # normalize
        capacity_risk = np.clip(capacity_risk, 0, 1)
        
        # 3. Sediment risk (direct from data)
        sediment_risk = self.nodes['sediment_risk'].values
        
        # 4. Hydraulic load risk (direct from data)
        load_risk = self.nodes['hydraulic_load'].values
        
        # Weighted combination
        w1, w2, w3, w4 = 0.25, 0.30, 0.25, 0.20
        
        self.hydraulic_vulnerability = (
            w1 * elevation_risk + 
            w2 * capacity_risk + 
            w3 * sediment_risk + 
            w4 * load_risk
        )
        
        # Normalize to [0, 1]
        self.hydraulic_vulnerability = (self.hydraulic_vulnerability - self.hydraulic_vulnerability.min())
        if self.hydraulic_vulnerability.max() > 0:
            self.hydraulic_vulnerability = self.hydraulic_vulnerability / self.hydraulic_vulnerability.max()
        
        print(f"  ✓ Hydraulic vulnerability computed")
        print(f"    Components:")
        print(f"    - Elevation risk: {w1*100:.0f}%")
        print(f"    - Capacity risk: {w2*100:.0f}%")
        print(f"    - Sediment risk: {w3*100:.0f}%")
        print(f"    - Load risk: {w4*100:.0f}%")
        print(f"    Range: [{self.hydraulic_vulnerability.min():.4f}, {self.hydraulic_vulnerability.max():.4f}]")
    
    def compute_integrated_vulnerability(self):
        """
        Integrate spectral and hydraulic factors for final vulnerability score
        
        Formula lengkap (BAB 2):
        Vul(i) = f(eigenvalue_centrality, degree_centrality, hydraulic_factors)
        
        Weights:
        - Eigenvalue centrality: 30% (spectral importance)
        - Degree centrality: 30% (topological importance)
        - Hydraulic vulnerability: 40% (physical constraints)
        """
        print("\n[8] Computing Integrated Vulnerability Scores...")
        
        # Weights for final combination
        w_eigen = 0.30
        w_degree = 0.30
        w_hydraulic = 0.40
        
        # Combined vulnerability
        self.vulnerability_scores = (
            w_eigen * self.eigenvalue_centrality +
            w_degree * self.degree_centrality +
            w_hydraulic * self.hydraulic_vulnerability
        )
        
        # Power transformation for better distribution
        self.vulnerability_scores = np.power(self.vulnerability_scores, 0.7)
        
        # Scale to max 0.95 (avoid perfect 1.0)
        self.vulnerability_scores = self.vulnerability_scores * (0.95 / self.vulnerability_scores.max())
        
        print(f"  ✓ Integrated vulnerability computed")
        print(f"    Weights:")
        print(f"    - Eigenvalue centrality: {w_eigen*100:.0f}%")
        print(f"    - Degree centrality: {w_degree*100:.0f}%")
        print(f"    - Hydraulic factors: {w_hydraulic*100:.0f}%")
        print(f"    Range: [{self.vulnerability_scores.min():.4f}, {self.vulnerability_scores.max():.4f}]")
    
    def classify_vulnerability(self):
        """
        Classify nodes into vulnerability categories
        """
        print("\n[9] Vulnerability Classification...")
        
        # Thresholds
        high_threshold = np.percentile(self.vulnerability_scores, 70)
        low_threshold = np.percentile(self.vulnerability_scores, 30)
        
        categories = []
        for score in self.vulnerability_scores:
            if score >= high_threshold:
                categories.append('high')
            elif score <= low_threshold:
                categories.append('low')
            else:
                categories.append('medium')
        
        n_high = categories.count('high')
        n_medium = categories.count('medium')
        n_low = categories.count('low')
        
        print(f"  ✓ Classification thresholds:")
        print(f"    - High: vulnerability ≥ {high_threshold:.3f}")
        print(f"    - Medium: {low_threshold:.3f} < vulnerability < {high_threshold:.3f}")
        print(f"    - Low: vulnerability ≤ {low_threshold:.3f}")
        
        print(f"\n  ✓ Distribution:")
        print(f"    - High vulnerability: {n_high} nodes ({n_high/len(categories)*100:.1f}%)")
        print(f"    - Medium vulnerability: {n_medium} nodes ({n_medium/len(categories)*100:.1f}%)")
        print(f"    - Low vulnerability: {n_low} nodes ({n_low/len(categories)*100:.1f}%)")
        
        return categories
    
    def generate_report(self):
        """
        Generate comprehensive report with all analysis results
        Returns dataframe to be saved by caller
        """
        print(f"\n[10] Generating Report...")
        
        # Classify vulnerability
        categories = self.classify_vulnerability()
        
        # Get node degrees
        degrees = np.sum(self.adj_matrix, axis=1).astype(int)
        
        # Create results dataframe
        results = pd.DataFrame({
            'node_id': self.nodes['node_id'],
            'latitude': self.nodes['latitude'],
            'longitude': self.nodes['longitude'],
            'type': self.nodes['type'],
            'degree': degrees,
            'eigenvalue_centrality': self.eigenvalue_centrality,
            'degree_centrality': self.degree_centrality,
            'hydraulic_vulnerability': self.hydraulic_vulnerability,
            'vulnerability_score': self.vulnerability_scores,
            'vulnerability_category': categories,
            'elevation': self.nodes['elevation'],
            'flow_capacity': self.nodes['flow_capacity'],
            'rainfall_intensity': self.nodes['rainfall_intensity'],
            'sediment_risk': self.nodes['sediment_risk'],
            'hydraulic_load': self.nodes['hydraulic_load'],
        })
        
        # Sort by vulnerability (descending)
        results = results.sort_values('vulnerability_score', ascending=False)
        
        print(f"  ✓ Report data generated")
        
        return results
    
    def print_top_vulnerable_nodes(self, results: pd.DataFrame, n: int = 15):
        """
        Print top N most vulnerable nodes with details
        """
        print(f"\n{'='*70}")
        print(f"TOP {n} MOST VULNERABLE NODES (Critical Bottlenecks)")
        print(f"{'='*70}")
        
        top_nodes = results.head(n)
        
        print(f"\n{'Node':<6} {'Deg':<5} {'Vuln':<7} {'Category':<10} {'Type':<12} {'Elev':<7} {'Capacity':<9} {'Rain':<7} {'Sediment':<9}")
        print("-"*86)
        
        for _, node in top_nodes.iterrows():
            print(f"{node['node_id']:<6} {node['degree']:<5} "
                  f"{node['vulnerability_score']:.3f}   "
                  f"{node['vulnerability_category']:<10} "
                  f"{node['type']:<12} "
                  f"{node['elevation']:>5.1f}m  "
                  f"{node['flow_capacity']:>6.1f}m³/s "
                  f"{node['rainfall_intensity']:>5.1f}mm/h "
                  f"{node['sediment_risk']:.3f}")
    
    def print_network_statistics(self):
        """
        Print comprehensive network statistics
        """
        print(f"\n{'='*70}")
        print("NETWORK STATISTICS SUMMARY")
        print(f"{'='*70}")
        
        print(f"\n📊 Spectral Properties:")
        print(f"  • Algebraic connectivity (λ₂): {self.algebraic_connectivity:.6f}")
        print(f"  • Spectral radius ρ(A): {self.spectral_radius:.6f}")
        print(f"  • Eigenvalue range: [{self.eigenvalues.min():.6f}, {self.eigenvalues.max():.6f}]")
        
        degrees = np.sum(self.adj_matrix, axis=1)
        print(f"\n🔗 Connectivity:")
        print(f"  • Average degree: {np.mean(degrees):.2f}")
        print(f"  • Max degree: {int(np.max(degrees))}")
        print(f"  • Min degree: {int(np.min(degrees))}")
        
        print(f"\n💧 Hydraulic Parameters:")
        print(f"  • Elevation: {self.nodes['elevation'].min():.1f} - {self.nodes['elevation'].max():.1f} m")
        print(f"  • Flow capacity: {self.nodes['flow_capacity'].min():.1f} - {self.nodes['flow_capacity'].max():.1f} m³/s")
        print(f"  • Rainfall: {self.nodes['rainfall_intensity'].min():.1f} - {self.nodes['rainfall_intensity'].max():.1f} mm/h")
        print(f"  • Sediment risk: {self.nodes['sediment_risk'].min():.3f} - {self.nodes['sediment_risk'].max():.3f}")
        
        print(f"\n⚠️ Vulnerability:")
        print(f"  • Score range: {self.vulnerability_scores.min():.3f} - {self.vulnerability_scores.max():.3f}")
        print(f"  • Mean: {np.mean(self.vulnerability_scores):.3f}")
        print(f"  • Std dev: {np.std(self.vulnerability_scores):.3f}")
    
    def run_complete_analysis(self):
        """
        Run complete analysis pipeline
        """
        self.load_data()
        self.construct_matrices()
        self.spectral_analysis()
        self.compute_spectral_radius()
        self.power_iteration_centrality()
        self.compute_degree_centrality()
        self.hydraulic_flow_analysis()
        self.compute_integrated_vulnerability()
        
        results = self.generate_report()
        
        self.print_network_statistics()
        self.print_top_vulnerable_nodes(results)
        
        print(f"\n{'='*70}")
        print("✓ ANALYSIS COMPLETE")
        print(f"{'='*70}")
        
        return results


if __name__ == "__main__":
    import os
    
    # Get absolute paths relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    nodes_file = os.path.join(project_root, 'data', 'nodes.csv')
    edges_file = os.path.join(project_root, 'data', 'edges.csv')
    output_file = os.path.join(project_root, 'hasil', 'results.csv')
    
    # Initialize analyzer
    analyzer = HydraulicDrainageAnalyzer(
        nodes_file=nodes_file,
        edges_file=edges_file
    )
    
    # Run complete analysis
    results = analyzer.run_complete_analysis()
    
    # Save with proper path
    results.to_csv(output_file, index=False)
    
    print(f"\n📁 Output files:")
    print(f"  • {output_file} - Complete analysis results")
