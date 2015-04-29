from support import RpgTestCase
from rpg import Base


class FunctionalTest(RpgTestCase):

    def test_c_project(self):
        base = Base()
        # base.conf.exclude.append("CPlugin")
        base.load_plugins()
        base.process_archive_or_dir(
            self.test_project_dir / "archives/hello-1.4.tar.gz")
        base.spec.Name = "hello"
        base.spec.Version = "1.4"
        base.spec.Release = "1%{?dist}"
        base.spec.License = "GPLv2"
        base.spec.Summary = "Hello World test program"
        base.spec.description = "desc"
        base.spec.build = "make"
        base.run_raw_sources_analysis()
        base.run_patched_sources_analysis()
        expected_requires = {
            "/usr/include/gnu",
            "/usr/include",
            "/usr/include/sys",
            "/usr/include/bits"
        }
        dirs = [
            "hello-1.4/Makefile", 
            "hello-1.4/hello.c",
            "hello-1.4/hello"
        ]
        self.assertEqual("make", str(base.spec.build))
        self.assertEqual(expected_requires, set(base.spec.Requires))
        self.assertEqual(expected_requires, set(base.spec.BuildRequires))
        self.assertExistInDir(["Makefile","hello.c"], base.extracted_dir)
        base.build_project()
        self.assertExistInDir(dirs, base.compiled_dir)
        self.assertEqual(
            (["hello-1.4/hello"], None, None), set(base.spec.files))
        print(str(base.spec))
        # base.run_compiled_analysis()
        # base.install_project()
        # base.run_installed_analysis()
        # base.create_spec_and_archive()
        # base.build_packages("fedora-21-x86_64")
        # self.assertEqual(base.spec.files, "")
