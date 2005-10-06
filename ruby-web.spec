%define	ruby_archdir	%(ruby -r rbconfig -e 'print Config::CONFIG["archdir"]')
%define	ruby_ridir	%(ruby -r rbconfig -e 'include Config; print File.join(CONFIG["datadir"], "ri", CONFIG["ruby_version"], "system")')
%define ruby_rubylibdir %(ruby -r rbconfig -e 'print Config::CONFIG["rubylibdir"]')
Summary:	A web platform for pages and applications
Name:		ruby-web
Version:	1.1.0
Release:	1
License:	Ruby's
Group:		Development/Languages
Source0:	http://rubyforge.org/frs/download.php/6307/%{name}_%{version}.beta.tar.gz
# Source0-md5:	c8d2ab1498618bc8272b3171a895c4ae
URL:		http://ruby-web.org
BuildRequires:	ruby
BuildRequires:	ruby-devel
BuildRequires:	setup.rb = 3.3.1
Requires:	ruby
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ruby-web is designed to create pages that scale to applications. ruby-web allows the use of an "application.rb" file to pull a site out of a directory of pages. There is extensive support for testing methods to help with the growing pains. Finally, ruby-web contains methods to support distribution of resources like images in a ruby library.

%prep
%setup -q -n %{name}-%{version}.beta

%build
cp %{_datadir}/setup.rb .

ruby setup.rb config \
	--rbdir=%{ruby_rubylibdir} \
	--sodir=%{ruby_archdir}

ruby setup.rb setup

rdoc --op rdoc lib
rdoc --ri --op ri lib

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_archdir},%{ruby_ridir}}

ruby setup.rb install \
	--prefix=$RPM_BUILD_ROOT

cp -a lib/web/resources/* $RPM_BUILD_ROOT/%{ruby_rubylibdir}/web/resources/

cp -a ri/ri/* $RPM_BUILD_ROOT%{ruby_ridir}
rm $RPM_BUILD_ROOT%{ruby_ridir}/Array/cdesc-Array.yaml
rm $RPM_BUILD_ROOT%{ruby_ridir}/Object/cdesc-Object.yaml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc rdoc
%attr(755,root,root) %{_bindir}/*
%{ruby_rubylibdir}/web.rb
%{ruby_rubylibdir}/web
%{ruby_ridir}/*
