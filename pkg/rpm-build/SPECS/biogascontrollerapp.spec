Name:           biogascontrollerapp
Version:        3.0
Release:        1%{?dist}
Summary:        Utility Software to control the Biogas plant of ENATECH at KSWO

License:        GPL
URL:            http://github.com/janishutz/BiogasControllerApp
Source0:        biogascontrollerapp-3.0.tar.gz

%description
Utility Software to control the Biogas plant of ENATECH at KSWO

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}/usr/local/bin
cp biogascontrollerapp %{buildroot}/usr/local/bin/

%files
/usr/local/bin/biogascontrollerapp

%changelog
