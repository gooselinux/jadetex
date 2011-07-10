Name: jadetex
Version: 3.13
Release: 8%{?dist}
Group: Applications/Publishing

Summary: TeX macros used by Jade TeX output

License: Freely redistributable without restriction
URL: http://sourceforge.net/projects/jadetex

Requires: sgml-common >= 0.5
Requires: texlive, tex(latex)
Requires: jade
Requires(post): texlive
Requires(post): policycoreutils
BuildRequires: unzip tex(latex) texlive texlive-fonts

BuildRoot: %{_tmppath}/%{name}-%{version}

BuildArch: noarch
Source0: http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1: jadefmtutil.cnf
Patch0: jadetex-tetex3.patch
Patch1: jadetex-3.13-typoupstream.patch


%description
JadeTeX contains the additional LaTeX macros necessary for taking Jade
TeX output files and processing them as TeX files (to obtain DVI,
PostScript, or PDF files, for example).

%prep
%setup -q
cp -p %{SOURCE1} .
%patch0 -p1 -b .tetex3
%patch1 -p1 -b .typoupstream

%build
make


%install
DESTDIR=$RPM_BUILD_ROOT
rm -rf $DESTDIR
mkdir -p $DESTDIR
make install DESTDIR=$DESTDIR

mkdir -p ${DESTDIR}%{_datadir}/texmf/tex/jadetex
cp -p *.ini ${DESTDIR}%{_datadir}/texmf/tex/jadetex
cp -p *.sty ${DESTDIR}%{_datadir}/texmf/tex/jadetex
cp -p *.cnf ${DESTDIR}%{_datadir}/texmf/tex/jadetex

mkdir -p ${DESTDIR}%{_bindir}
ln -s etex ${DESTDIR}%{_bindir}/jadetex
ln -s pdfetex ${DESTDIR}%{_bindir}/pdfjadetex

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
cp -p jadetex.1 ${RPM_BUILD_ROOT}%{_mandir}/man1
ln -s jadetex.1.gz ${RPM_BUILD_ROOT}%{_mandir}/man1/pdfjadetex.1

%clean
DESTDIR=$RPM_BUILD_ROOT
rm -rf $DESTDIR


%post
[ -x %{_bindir}/texconfig-sys ] && %{_bindir}/texconfig-sys rehash 2> /dev/null || :
%{_bindir}/env - PATH=$PATH:%{_bindir} fmtutil-sys --cnffile %{_datadir}/texmf/tex/jadetex/jadefmtutil.cnf --all --fmtdir %{_datadir}/texmf/web2c > /dev/null 2>&1
rm -f %{_datadir}/texmf/web2c/jadetex.log
rm -f %{_datadir}/texmf/web2c/pdfjadetex.log
restorecon -R /usr/share/texmf/web2c
exit 0

%postun
[ -x %{_bindir}/texconfig-sys ] && %{_bindir}/texconfig-sys rehash 2> /dev/null || :


%files
%defattr(-,root,root,-)
%doc index.html
%ghost %{_datadir}/texmf/web2c/jadetex.fmt
%ghost %{_datadir}/texmf/web2c/pdfjadetex.fmt
%dir %{_datadir}/texmf/tex/jadetex
%{_datadir}/texmf/tex/jadetex/dsssl.def
%{_datadir}/texmf/tex/jadetex/jadetex.ltx
%{_datadir}/texmf/tex/jadetex/jadetex.ini
%{_datadir}/texmf/tex/jadetex/pdfjadetex.ini
%{_datadir}/texmf/tex/jadetex/dummyels.sty
%{_datadir}/texmf/tex/jadetex/mlnames.sty
%{_datadir}/texmf/tex/jadetex/ucharacters.sty
%{_datadir}/texmf/tex/jadetex/uentities.sty
%{_datadir}/texmf/tex/jadetex/unicode.sty
%{_datadir}/texmf/tex/jadetex/jadefmtutil.cnf
%{_mandir}/man1/jadetex.1*
%{_mandir}/man1/pdfjadetex.1*
%{_bindir}/jadetex
%{_bindir}/pdfjadetex

%triggerin -- texlive
/usr/bin/env - PATH=$PATH:%{_bindir} fmtutil-sys --cnffile %{_datadir}/texmf/tex/jadetex/jadefmtutil.cnf --all > /dev/null 2>&1
exit 0

%changelog
* Fri Aug 28 2009 Ondrej Vasik <ovasik@redhat.com> 3.13-8
- ship manpage for jadetex/pdfjadetex

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Ondrej Vasik  <ovasik@redhat.com> 3.13-6
- fix requires(to match TeXLive2008 provides)
- trigger change to texlive

* Tue Mar 10 2009 Ondrej Vasik  <ovasik@redhat.com> 3.13-5
- cleanup after post scriptlet (no .log files in web2c dir)

* Mon Mar  9 2009 Ondrej Vasik  <ovasik@redhat.com> 3.13-4
- run restorecon -R /usr/share/texmf/web2c in post to prevent
  mishandled context (#448101)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan  7 2008 Ondrej Vasik  <ovasik@redhat.com> 3.13-2
- removed TeXdir macro, replaced by /usr(in fact by other
  rpm macros)
- used texcongig-sys rehash instead of texhash
- added documentation html file
- dist tag, license fix

* Fri Jun  8 2007 Ondrej Vasik  <ovasik@redhat.com> 3.13-1
- update to latest upstream version( 3.13)
- removed jadetex-3.12-theta.patch(included in 3.13)
- added small typo fix from upstream

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: kpsewhich: command not found
- rebuild

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 3.12-13
- Use fmtutil-sys instead of fmtutil (bug #150089).
- Require at least teTeX 3.

* Wed Feb 23 2005 Tim Waugh <twaugh@redhat.com> 3.12-12
- Applied fixes from Ulrich Drepper to work with tetex3 (bug #111309).

* Tue Sep 14 2004 Tim Waugh <twaugh@redhat.com> 3.12-11
- Build requires tetex-fonts (bug #132529).

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Dec 30 2002 Karsten Hopp <karsten@redhat.de> 3.12-8
- BuildPrereq tetex (for kpsewhich)

* Wed Nov 20 2002 Tim Powers <timp@redhat.com>
- rebuild in current collinst

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 3.12-6
- build using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 3.12-5
- automated rebuild

* Fri Jun 21 2002 Tim Waugh <twaugh@redhat.com> 3.12-4
- Fix theta problem (bug #64865).

* Thu May 23 2002 Tim Powers <timp@redhat.com> 3.12-3
- automated rebuild

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 3.12-2
- Rebuild in new environment.

* Fri Jan 25 2002 Tim Waugh <twaugh@redhat.com> 3.12-1
- 3.12.
- Patches no longer needed: makefile, emergency, exp, multicols, euro,
  twosides.

* Fri Jan 11 2002 Tim Waugh <twaugh@redhat.com> 3.11-8
- Fix euro support.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 3.11-7
- automated rebuild

* Thu Jan  3 2002 Tim Waugh <twaugh@redhat.com> 3.11-6
- Build requires tetex-latex (bug #57895).

* Tue Dec 18 2001 Tim Waugh <twaugh@redhat.com> 3.11-5
- Ian Castle figured out how to fix unbalanced columns.  Apply
  his sourceforge patch.

* Wed Dec 12 2001 Tim Waugh <twaugh@redhat.com> 3.11-4
- Trigger on tetex-latex, not the base tetex package.

* Wed Oct 31 2001 Tim Waugh <twaugh@redhat.com> 3.11-3
- Revert the multicols change in 3.11 until the reason it breaks
  DocBook indexes is discovered.

* Mon Oct  1 2001 Tim Waugh <twaugh@redhat.com> 3.11-2
- Own /usr/share/texmf/tex/jadetex (bug #51381).

* Tue Sep 11 2001 Tim Waugh <twaugh@redhat.com> 3.11-1
- 3.11 (bug #51951).
- Trigger: rebuild fmt when teTeX is upgraded (bug #51921).

* Tue Aug 14 2001 Tim Powers <timp@redhat.com> 3.6-4
- rebuilt to hopefully fix rpm verify problems

* Thu Aug  9 2001 Tim Waugh <twaugh@redhat.com> 3.6-3
- Use %%ghost for the fmt files, since they get recreated (bug #49580).

* Wed Aug  1 2001 Tim Waugh <twaugh@redhat.com> 3.6-2
- Use emergencystretch (bug #47345).

* Mon Jun  4 2001 Tim Waugh <twaugh@redhat.com> 3.6-1
- 3.6.

* Mon Feb 12 2001 Tim Waugh <twaugh@redhat.com> 3.3-1
- 3.3.  Redo jadetex-makefile.patch.

* Fri Jan 19 2001 Tim Waugh <twaugh@redhat.com>
- Earlier change was wrong; jade should be required, not openjade
- Require sgml-common >= 0.5.

* Wed Jan 17 2001 Tim Waugh <twaugh@redhat.com>
- Make tetex a %%post requirement.
- Silence %%post output.
- Don't play so many macro games.
- Build requires unzip.

* Fri Jan 12 2001 Tim Waugh <twaugh@redhat.com>
- Make symlinks relative.

* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- Change group.
- Require openjade not jade.
- rm before install.
- Use %%{_tmppath}.
- Require tetex-latex.
- Change Copyright: to License:.
- Remove Packager: line.

* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- Based on Eric Bischoff's new-trials packages.
