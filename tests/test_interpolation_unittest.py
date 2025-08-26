#!/usr/bin/env python
"""
Unit tests for limbdark interpolation functionality using unittest.
Tests the LDInterpolator class and verifies smooth interpolation behavior.
"""

import unittest
import numpy as np
from limbdark.interpolator import LDInterpolator


class TestLDInterpolator(unittest.TestCase):
    """Test suite for LDInterpolator class using unittest."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.interpolator_linear = LDInterpolator('T', kind='linear')
        self.interpolator_nearest = LDInterpolator('T', kind='nearest')
        
        # Create test grids
        teff_vals = np.linspace(4500, 5500, 21)
        logg_vals = np.linspace(4, 5, 21)
        self.test_grid = np.meshgrid(teff_vals, logg_vals)
        
        teff_vals_small = np.linspace(4500, 5500, 5)
        logg_vals_small = np.linspace(4, 5, 5)
        self.small_grid = np.meshgrid(teff_vals_small, logg_vals_small)

    def test_interpolator_initialization(self):
        """Test that interpolators can be initialized correctly."""
        # Test different bands
        ldi_t = LDInterpolator('T')
        self.assertEqual(ldi_t.band, 'T')
        self.assertEqual(ldi_t.law, 'quadratic')  # default
        
        ldi_kp = LDInterpolator('Kp', law='linear')
        self.assertEqual(ldi_kp.band, 'Kp')
        self.assertEqual(ldi_kp.law, 'linear')
    
    def test_interpolator_call_basic(self):
        """Test basic interpolator functionality with single values."""
        # Test single point interpolation
        teff, logg, feh = 5000, 4.5, 0.0
        result = self.interpolator_linear(teff, logg, feh)
        
        # Should return 2 values for quadratic law (u1, u2)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(np.isscalar(val) or (hasattr(val, 'shape') and val.shape == ()) for val in result))
        self.assertTrue(all(np.isfinite(val) for val in result))
    
    def test_interpolator_call_arrays(self):
        """Test interpolator with array inputs."""
        X, Y = self.small_grid
        feh = 0.0
        
        U, V = self.interpolator_linear(X, Y, feh)
        
        # Check output shapes match input
        self.assertEqual(U.shape, X.shape)
        self.assertEqual(V.shape, Y.shape)
        self.assertEqual(U.shape, (5, 5))
        
        # Check all values are finite
        self.assertTrue(np.all(np.isfinite(U)))
        self.assertTrue(np.all(np.isfinite(V)))
    
    def test_interpolation_smoothness_linear(self):
        """Test that linear interpolation produces smooth results."""
        X, Y = self.test_grid
        feh = 0.0
        
        U, V = self.interpolator_linear(X, Y, feh)
        
        # Check that we get high resolution (many unique values)
        # For a 21x21 grid, we should get close to 441 unique values with smooth interpolation
        unique_u = len(np.unique(U))
        unique_v = len(np.unique(V))
        
        # Should have significantly more unique values than the underlying data grid (~25 points)
        self.assertGreater(unique_u, 100, 
                          f"Linear interpolation should produce many unique values, got {unique_u}")
        self.assertGreater(unique_v, 100, 
                          f"Linear interpolation should produce many unique values, got {unique_v}")
        
        # Should be close to the theoretical maximum (441 for 21x21 grid)
        self.assertGreater(unique_u, 400, 
                          f"Linear interpolation should be nearly smooth, got {unique_u}/441 unique values")
        self.assertGreater(unique_v, 400, 
                          f"Linear interpolation should be nearly smooth, got {unique_v}/441 unique values")
    
    def test_interpolation_smoothness_nearest(self):
        """Test that nearest-neighbor interpolation produces blocky results."""
        X, Y = self.test_grid
        feh = 0.0
        
        U, V = self.interpolator_nearest(X, Y, feh)
        
        # Check that nearest-neighbor gives fewer unique values (blocky)
        unique_u = len(np.unique(U))
        unique_v = len(np.unique(V))
        
        # Should have significantly fewer unique values than linear interpolation
        self.assertLess(unique_u, 100, 
                       f"Nearest interpolation should produce fewer unique values, got {unique_u}")
        self.assertLess(unique_v, 100, 
                       f"Nearest interpolation should produce fewer unique values, got {unique_v}")
    
    def test_interpolation_comparison(self):
        """Test that linear interpolation is smoother than nearest-neighbor."""
        X, Y = self.test_grid
        feh = 0.0
        
        # Create both interpolators
        ldi_linear = LDInterpolator('T', kind='linear')
        ldi_nearest = LDInterpolator('T', kind='nearest')
        
        # Get results
        U_linear, V_linear = ldi_linear(X, Y, feh)
        U_nearest, V_nearest = ldi_nearest(X, Y, feh)
        
        # Linear should have more unique values than nearest
        self.assertGreater(len(np.unique(U_linear)), len(np.unique(U_nearest)))
        self.assertGreater(len(np.unique(V_linear)), len(np.unique(V_nearest)))
    
    def test_interpolation_bounds(self):
        """Test interpolation within reasonable parameter bounds."""
        # Test various points within the expected parameter space
        test_points = [
            (4000, 4.0, -0.5),  # Cool star
            (5000, 4.5, 0.0),   # Sun-like
            (6000, 4.0, 0.3),   # Hot star
        ]
        
        for teff, logg, feh in test_points:
            result = self.interpolator_linear(teff, logg, feh)
            self.assertEqual(len(result), 2)
            self.assertTrue(all(np.isfinite(val) for val in result))
            
            # Limb darkening coefficients should be reasonable
            u1, u2 = result
            self.assertGreaterEqual(u1, 0, f"u1 should be >= 0, got {u1}")
            self.assertLessEqual(u1, 1, f"u1 should be <= 1, got {u1}")
            self.assertGreaterEqual(u2, 0, f"u2 should be >= 0, got {u2}")
            self.assertLessEqual(u2, 1, f"u2 should be <= 1, got {u2}")
    
    def test_different_laws(self):
        """Test different limb darkening laws."""
        laws = ['linear', 'quadratic', 'squareroot', 'logarithmic', 'nonlinear']
        expected_outputs = [1, 2, 2, 2, 4]  # Number of coefficients for each law
        
        for law, expected_n in zip(laws, expected_outputs):
            ldi = LDInterpolator('T', law=law)
            result = ldi(5000, 4.5, 0.0)
            self.assertEqual(len(result), expected_n, 
                           f"Law {law} should return {expected_n} coefficients")
            self.assertTrue(all(np.isfinite(val) for val in result))
    
    def test_different_bands(self):
        """Test different photometric bands."""
        bands = ['T', 'Kp', 'V', 'I']  # Sample of available bands
        
        for band in bands:
            ldi = LDInterpolator(band)
            result = ldi(5000, 4.5, 0.0)
            self.assertEqual(len(result), 2)  # quadratic law default
            self.assertTrue(all(np.isfinite(val) for val in result))
    
    def test_metallicity_variation(self):
        """Test interpolation across different metallicities."""
        teff, logg = 5000, 4.5
        metallicities = [-0.5, 0.0, 0.3]
        
        results = []
        for feh in metallicities:
            result = self.interpolator_linear(teff, logg, feh)
            results.append(result)
            self.assertEqual(len(result), 2)
            self.assertTrue(all(np.isfinite(val) for val in result))
        
        # Results should vary with metallicity
        u1_values = [r[0] for r in results]
        u2_values = [r[1] for r in results]
        
        # Should have some variation (not all identical)
        self.assertGreater(len(set(np.round(u1_values, 4))), 1, 
                          "u1 should vary with metallicity")
        self.assertGreater(len(set(np.round(u2_values, 4))), 1, 
                          "u2 should vary with metallicity")


class TestInterpolationQuality(unittest.TestCase):
    """Additional tests for interpolation quality and edge cases."""
    
    def test_grid_resolution_scaling(self):
        """Test that interpolation quality scales with grid resolution."""
        ldi = LDInterpolator('T', kind='linear')
        feh = 0.0
        
        # Test different grid resolutions
        resolutions = [5, 11, 21]
        unique_counts = []
        
        for res in resolutions:
            teff_vals = np.linspace(4500, 5500, res)
            logg_vals = np.linspace(4, 5, res)
            X, Y = np.meshgrid(teff_vals, logg_vals)
            
            U, V = ldi(X, Y, feh)
            unique_u = len(np.unique(U))
            unique_counts.append(unique_u)
        
        # Higher resolution should generally give more unique values
        self.assertGreater(unique_counts[1], unique_counts[0], 
                          "Higher resolution should give more unique values")
        self.assertGreater(unique_counts[2], unique_counts[1], 
                          "Higher resolution should give more unique values")
    
    def test_interpolation_continuity(self):
        """Test that interpolation is continuous (no sudden jumps)."""
        ldi = LDInterpolator('T', kind='linear')
        
        # Create a fine grid around a central point
        teff_center, logg_center, feh = 5000, 4.5, 0.0
        delta = 50  # Small perturbation
        
        # Test points around the center
        points = [
            (teff_center, logg_center),
            (teff_center + delta, logg_center),
            (teff_center, logg_center + 0.1),
            (teff_center + delta, logg_center + 0.1),
        ]
        
        results = []
        for teff, logg in points:
            result = ldi(teff, logg, feh)
            results.append(result)
        
        # Check that nearby points give similar results (continuity)
        for i in range(len(results) - 1):
            u1_diff = abs(results[i][0] - results[i+1][0])
            u2_diff = abs(results[i][1] - results[i+1][1])
            
            # Differences should be small for nearby points
            self.assertLess(u1_diff, 0.1, f"Large discontinuity in u1: {u1_diff}")
            self.assertLess(u2_diff, 0.1, f"Large discontinuity in u2: {u2_diff}")


def run_tests():
    """Run all tests and print results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLDInterpolator))
    suite.addTests(loader.loadTestsFromTestCase(TestInterpolationQuality))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\nRan {result.testsRun} tests")
    if result.wasSuccessful():
        print("All tests passed!")
    else:
        print(f"Failed: {len(result.failures)} tests")
        print(f"Errors: {len(result.errors)} tests")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()