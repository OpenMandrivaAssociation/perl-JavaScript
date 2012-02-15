%define upstream_name	JavaScript
%define upstream_version 1.16

Name:       perl-%{upstream_name}
Version:    %perl_convert_version %{upstream_version}
Release:	4

Summary:	Execute JavaScript from within Perl
License:	Artistic or GPL 
Group:		Development/Perl
Url:		http://search.cpan.org/dist/%{upstream_name}/
Source0:	ftp://ftp.perl.org/pub/CPAN/modules/by-module/JavaScript/%{upstream_name}-%{upstream_version}.tar.gz
Patch0:     JavaScript-1.12-fix-inline-c-inc-from-jsinc.patch

%define do_test 1
%{?_without_test:           %global do_test 0}
%{?_with_test:              %global do_test 1}

Buildrequires:	libjs-devel
Buildrequires:	libnspr-devel
Buildrequires:	perl-devel
Buildrequires:	pkgconfig
Buildrequires:	sed
%if %do_test
Buildrequires:	perl(Test::Exception)
%endif

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}

%description
JavaScript.pm is an interface to the SpiderMonkey JS engine. It lets you execute JS code, 
call JS functions, bind Perl classes to JS, import Perl functions to JS, precompile and exeute 
scripts among many other things. It does conversion between Perl and JS datatypes.

  use JavaScript;

  my $rt = JavaScript::Runtime->new();
  my $cx = $rt->create_context();

  $cx->bind_function(write => sub { print @_; });

  $cx->eval(q/
    for (i = 99; i > 0; i--) {
        write(i + " bottle(s) of beer on the wall, " + i + " bottle(s) of beer\n");
        write("Take 1 down, pass it around, ");
        if (i > 1) {
            write((i - 1) + " bottle(s) of beer on the wall.");
        }
        else {
            write("No more bottles of beer on the wall!");
        }
    }
  /);


%package devel
Summary:  Perl JavaScript development files
Group:    Development/Perl
Requires: %{name} = %{version}
Requires: libjs-devel

%description devel
Development files for extending Perl Javascript 
or for testing JavaScript code from Perl.


%prep
%setup -q -n %{upstream_name}-%{upstream_version}
%patch0 -p0 -b .fix-inc
%define jsinc   %(eval echo $(pkg-config libjs --cflags-only-I | sed s/-I//))
%define nsprinc %(eval echo $(pkg-config nspr --cflags-only-I  | sed s/-I//))
%define JS_INC %{jsinc}:%{nsprinc}

%build
JS_INC=%{JS_INC} JS_THREADSAFE=1 JS_UTF8=0 JS_ENABLE_E4X=1 %{__perl} Makefile.PL
perl -pi -e's|/usr/local/share/man/man3|/usr/share/man/man3|' Makefile
%make CFLAGS="%{optflags}" 

%install
rm -rf %{buildroot}
%makeinstall_std 

%check
%if %do_test
JS_INC=%{JS_INC} %{__make} test
%endif

%clean 
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%{perl_sitearch}/JavaScript
%{perl_sitearch}/JavaScript.pm
%dir %{perl_sitearch}/auto/JavaScript
%{perl_sitearch}/auto/JavaScript/JavaScript.so
%{_mandir}/man3/JavaScript*

%files devel
%defattr(-,root,root)
%{perl_sitearch}/Test
%{perl_sitearch}/auto/JavaScript/*.h
%{perl_sitearch}/auto/JavaScript/typemap
%{_mandir}/man3/Test::*

