#!/usr/bin/env python3
"""
Python Version Enforcement Script
File: scripts/check_python_version.py

Ensures Python 3.13.5+ is being used before running the AI Test Case Generator.
This script should be run before any main application code.
"""

import sys
import platform
import subprocess
from pathlib import Path
from typing import Tuple, List

# Minimum required version
REQUIRED_VERSION = (3, 13, 5)
PROJECT_NAME = "AI Test Case Generator"

class VersionChecker:
    """Handles Python version validation and dependency checking"""
    
    def __init__(self, required_version: Tuple[int, int, int] = REQUIRED_VERSION):
        self.required_version = required_version
        self.current_version = sys.version_info[:3]
    
    def check_python_version(self) -> bool:
        """
        Check if current Python version meets requirements
        
        Returns:
            bool: True if version is acceptable, False otherwise
        """
        print(f"🐍 Python Version Check for {PROJECT_NAME}")
        print("=" * 60)
        
        current_str = ".".join(map(str, self.current_version))
        required_str = ".".join(map(str, self.required_version))
        
        print(f"📊 Current Python: {sys.version}")
        print(f"📍 Platform: {platform.platform()}")
        print(f"🏗️  Architecture: {platform.architecture()[0]}")
        print(f"🎯 Required: Python >= {required_str}")
        print(f"🔍 Detected: Python {current_str}")
        
        if self.current_version >= self.required_version:
            print(f"✅ Version check PASSED")
            return True
        else:
            print(f"❌ Version check FAILED")
            self._print_upgrade_instructions()
            return False
    
    def _print_upgrade_instructions(self) -> None:
        """Print detailed upgrade instructions"""
        required_str = ".".join(map(str, self.required_version))
        current_str = ".".join(map(str, self.current_version))
        
        print("\n🚨 Python Version Insufficient")
        print("=" * 60)
        print(f"Current: Python {current_str}")
        print(f"Required: Python >= {required_str}")
        print()
        print("💡 Why Python 3.13.5+ is required:")
        print("   • Enhanced error handling and diagnostics")
        print("   • Improved performance for file processing")
        print("   • Better typing support for code quality")
        print("   • Security improvements for production use")
        print("   • Future-proofing for upcoming features")
        print()
        print("🔧 How to upgrade:")
        print()
        
        # Platform-specific instructions
        system = platform.system().lower()
        
        if system == "windows":
            print("📦 Windows:")
            print("   1. Download Python 3.13.5+ from https://python.org/downloads/")
            print("   2. Run installer with 'Add to PATH' checked")
            print("   3. Restart terminal and run this check again")
            print("   Alternative: Use Windows Store or Chocolatey")
            print("      choco install python --version=3.13.5")
        
        elif system == "darwin":  # macOS
            print("🍎 macOS:")
            print("   Option 1 - Homebrew (recommended):")
            print("      brew install python@3.13")
            print("   Option 2 - Official installer:")
            print("      Download from https://python.org/downloads/")
            print("   Option 3 - pyenv:")
            print("      pyenv install 3.13.5")
            print("      pyenv global 3.13.5")
        
        elif system == "linux":
            print("🐧 Linux:")
            print("   Ubuntu/Debian:")
            print("      sudo apt update")
            print("      sudo apt install python3.13")
            print("   CentOS/RHEL/Fedora:")
            print("      sudo dnf install python3.13")
            print("   Arch Linux:")
            print("      sudo pacman -S python")
            print("   Universal - pyenv:")
            print("      curl https://pyenv.run | bash")
            print("      pyenv install 3.13.5")
        
        print("\n🔄 After upgrading:")
        print(f"   python3 --version  # Should show >= {required_str}")
        print(f"   python3 scripts/check_python_version.py  # Run this check again")
    
    def check_required_features(self) -> bool:
        """
        Check for specific Python 3.13.5+ features
        
        Returns:
            bool: True if all features are available
        """
        print(f"\n🔧 Feature Availability Check")
        print("=" * 60)
        
        features_passed = 0
        total_features = 0
        
        # Check 1: Enhanced error handling
        total_features += 1
        try:
            # Test improved syntax error reporting
            compile('x = 1\ny = x +', '<test>', 'exec')
        except SyntaxError as e:
            if hasattr(e, 'end_lineno') and hasattr(e, 'end_col_offset'):
                print("✅ Enhanced error reporting available")
                features_passed += 1
            else:
                print("⚠️ Basic error reporting only")
        
        # Check 2: Advanced typing features
        total_features += 1
        try:
            from typing import TypeVar, Generic, TypeAlias, Self
            print("✅ Advanced typing support available")
            features_passed += 1
        except ImportError:
            print("❌ Advanced typing features missing")
        
        # Check 3: Enhanced pathlib
        total_features += 1
        try:
            from pathlib import Path
            if hasattr(Path, 'walk'):  # Python 3.12+
                print("✅ Enhanced pathlib with walk() method")
                features_passed += 1
            else:
                print("⚠️ Basic pathlib (missing walk method)")
        except ImportError:
            print("❌ Pathlib not available")
        
        # Check 4: Performance improvements
        total_features += 1
        try:
            # Check for sys.monitoring (Python 3.12+)
            import sys
            if hasattr(sys, 'monitoring'):
                print("✅ Performance monitoring available")
                features_passed += 1
            else:
                print("⚠️ Performance monitoring not available")
        except:
            print("❌ Performance features missing")
        
        # Check 5: Security enhancements
        total_features += 1
        try:
            import hashlib
            # Check for newer hash algorithms
            if 'sha3_256' in hashlib.algorithms_available:
                print("✅ Enhanced security algorithms available")
                features_passed += 1
            else:
                print("⚠️ Limited security algorithms")
        except:
            print("❌ Security features missing")
        
        print("=" * 60)
        print(f"📊 Feature Check: {features_passed}/{total_features} features available")
        
        if features_passed == total_features:
            print("🎉 All Python 3.13.5+ features are available!")
            return True
        elif features_passed >= total_features * 0.8:  # 80% threshold
            print("⚠️ Most features available, but some optimizations missing")
            return True
        else:
            print("❌ Critical features missing - upgrade required")
            return False
    
    def check_dependencies(self, requirements_file: str = "requirements.txt") -> bool:
        """
        Check if all required dependencies are available and compatible
        
        Args:
            requirements_file: Path to requirements.txt file
            
        Returns:
            bool: True if all dependencies are satisfied
        """
        print(f"\n📦 Dependency Check")
        print("=" * 60)
        
        req_file_path = Path(requirements_file)
        if not req_file_path.exists():
            print(f"⚠️ Requirements file not found: {requirements_file}")
            return self._check_core_dependencies()
        
        try:
            # Read requirements file
            with open(req_file_path, 'r') as f:
                requirements = f.readlines()
            
            # Parse requirements (basic parsing)
            parsed_requirements = []
            for line in requirements:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('-'):
                    # Extract package name and version
                    if '>=' in line:
                        package, version = line.split('>=')[0], line.split('>=')[1].split(',')[0]
                        parsed_requirements.append((package.strip(), version.strip()))
                    elif '==' in line:
                        package, version = line.split('==')
                        parsed_requirements.append((package.strip(), version.strip()))
                    else:
                        # No version specified
                        parsed_requirements.append((line.strip(), None))
            
            return self._validate_parsed_requirements(parsed_requirements)
            
        except Exception as e:
            print(f"❌ Error reading requirements file: {e}")
            return self._check_core_dependencies()
    
    def _validate_parsed_requirements(self, requirements: List[Tuple[str, str]]) -> bool:
        """Validate parsed requirements against installed packages"""
        import pkg_resources
        
        all_satisfied = True
        missing_packages = []
        version_conflicts = []
        
        print(f"🔍 Checking {len(requirements)} requirements...")
        
        for package, min_version in requirements:
            try:
                installed = pkg_resources.get_distribution(package)
                installed_version = installed.version
                
                if min_version:
                    # Simple version comparison
                    def version_tuple(v):
                        return tuple(map(int, v.replace('rc', '').replace('a', '').replace('b', '').split('.')[:3]))
                    
                    try:
                        if version_tuple(installed_version) >= version_tuple(min_version):
                            print(f"✅ {package}: {installed_version} (>= {min_version})")
                        else:
                            print(f"❌ {package}: {installed_version} (< {min_version} required)")
                            version_conflicts.append((package, installed_version, min_version))
                            all_satisfied = False
                    except ValueError:
                        # Version parsing failed, just check presence
                        print(f"⚠️ {package}: {installed_version} (version format unclear)")
                else:
                    print(f"✅ {package}: {installed_version}")
                    
            except pkg_resources.DistributionNotFound:
                print(f"❌ {package}: NOT INSTALLED")
                missing_packages.append(package)
                all_satisfied = False
        
        # Summary
        if missing_packages:
            print(f"\n📋 Missing packages ({len(missing_packages)}):")
            for package in missing_packages:
                print(f"   • {package}")
            print("\n💡 Install missing packages:")
            print(f"   pip install {' '.join(missing_packages)}")
        
        if version_conflicts:
            print(f"\n⚠️ Version conflicts ({len(version_conflicts)}):")
            for package, current, required in version_conflicts:
                print(f"   • {package}: {current} < {required}")
            print("\n💡 Upgrade conflicting packages:")
            upgrade_list = [f"{pkg}>={req}" for pkg, _, req in version_conflicts]
            print(f"   pip install --upgrade {' '.join(upgrade_list)}")
        
        return all_satisfied
    
    def _check_core_dependencies(self) -> bool:
        """Check core dependencies without requirements file"""
        core_packages = {
            'pandas': '2.2.0',
            'requests': '2.31.0',
            'PyYAML': '6.0.1',
            'click': '8.1.7',
            'rich': '13.7.0'
        }
        
        print("🔍 Checking core dependencies...")
        
        import pkg_resources
        all_satisfied = True
        
        for package, min_version in core_packages.items():
            try:
                installed = pkg_resources.get_distribution(package)
                print(f"✅ {package}: {installed.version}")
            except pkg_resources.DistributionNotFound:
                print(f"❌ {package}: NOT INSTALLED")
                all_satisfied = False
        
        return all_satisfied
    
    def run_comprehensive_check(self) -> bool:
        """
        Run all checks and return overall status
        
        Returns:
            bool: True if all checks pass
        """
        print(f"🚀 Comprehensive Python Environment Check")
        print(f"🎯 Project: {PROJECT_NAME}")
        print("=" * 80)
        
        # Check 1: Python version
        version_ok = self.check_python_version()
        
        if not version_ok:
            print("\n🛑 CRITICAL: Python version check failed!")
            print("   Please upgrade Python before proceeding.")
            return False
        
        # Check 2: Python features
        features_ok = self.check_required_features()
        
        # Check 3: Dependencies
        deps_ok = self.check_dependencies()
        
        # Final summary
        print("\n" + "=" * 80)
        print("📊 FINAL VALIDATION SUMMARY")
        print("=" * 80)
        
        status_items = [
            ("Python Version", version_ok),
            ("Python Features", features_ok), 
            ("Dependencies", deps_ok)
        ]
        
        all_passed = True
        for item, status in status_items:
            icon = "✅" if status else "❌"
            print(f"{icon} {item}: {'PASSED' if status else 'FAILED'}")
            if not status:
                all_passed = False
        
        print("=" * 80)
        
        if all_passed:
            print("🎉 ALL CHECKS PASSED!")
            print(f"✅ Environment is ready for {PROJECT_NAME}")
            print("\n💡 You can now run:")
            print("   python src/generate_contextual_tests_v002.py --validate-prompts")
            print("   python src/generate_contextual_tests_v002.py input.reqifz")
        else:
            print("🚨 VALIDATION FAILED!")
            print("❌ Environment is not ready - please fix the issues above")
            print("\n🔧 Next steps:")
            if not version_ok:
                print("   1. Upgrade Python to 3.13.5 or higher")
            if not features_ok:
                print("   2. Verify Python installation completeness")
            if not deps_ok:
                print("   3. Install missing dependencies: pip install -r requirements.txt")
        
        return all_passed


def main():
    """Main entry point for version checking"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Python Version and Environment Checker for AI Test Case Generator"
    )
    parser.add_argument(
        "--requirements",
        default="requirements.txt",
        help="Path to requirements.txt file (default: requirements.txt)"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error code if any check fails"
    )
    parser.add_argument(
        "--version-only",
        action="store_true",
        help="Check only Python version (skip features and dependencies)"
    )
    
    args = parser.parse_args()
    
    checker = VersionChecker()
    
    if args.version_only:
        success = checker.check_python_version()
    else:
        success = checker.run_comprehensive_check()
    
    if args.strict and not success:
        print(f"\n💥 Exiting with error code due to failed checks")
        sys.exit(1)
    elif not success:
        print(f"\n⚠️ Checks failed but continuing (use --strict to exit on failure)")
        sys.exit(0)
    else:
        print(f"\n🎯 All checks passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()