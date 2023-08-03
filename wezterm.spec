%define raw_version %(unset https_proxy && curl -s https://api.github.com/repos/wez/wezterm/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")')

Name:           wezterm
Version:        %(unset https_proxy && curl -s https://api.github.com/repos/wez/wezterm/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")' | sed  's/-/./g')
Release:        1
URL:            https://github.com/wez/wezterm
Source0:        https://github.com/wez/wezterm/releases/download/%{raw_version}/wezterm-%{raw_version}-src.tar.gz#/%{name}-%{version}.tar.gz
Summary:        A GPU-accelerated cross-platform terminal emulator and multiplexer
License:        Apache-2.0
BuildRequires:  rustc
BuildRequires:  pkg-config
BuildRequires:  libxcb-dev xcb-proto-dev xcb-util-cursor-dev xcb-util-xrm-dev
BuildRequires:  freetype-dev
BuildRequires:  xclip
BuildRequires:  fontconfig-dev
BuildRequires:  mesa-dev
BuildRequires:  libxkbcommon-dev
BuildRequires:  ncurses-dev
BuildRequires:  python3
BuildRequires:  libssh2-dev
BuildRequires:  wayland-dev
BuildRequires:  wayland-protocols-dev
BuildRequires:  harfbuzz-dev
BuildRequires:  libgit2-dev
BuildRequires:  openssl-dev
  

 
%description
A GPU-accelerated cross-platform terminal emulator and multiplexer.

%prep
unset https_proxy
%setup -q -n %{name}-%(curl -s  https://api.github.com/repos/wez/wezterm/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")')

%build
unset http_proxy https_proxy no_proxy
export RUSTFLAGS="$RUSTFLAGS -C target-cpu=westmere -C target-feature=+avx -C opt-level=3 -C codegen-units=1 -C panic=abort -Clink-arg=-Wl,-z,now,-z,relro,-z,max-page-size=0x4000,-z,separate-code "
cargo build --release --all-features


%install
install -Dm755 target/release/wezterm %{buildroot}/usr/bin/wezterm
install -Dm755 target/release/wezterm-gui %{buildroot}/usr/bin/wezterm-gui
install -Dm755 target/release/wezterm-mux-server %{buildroot}/usr/bin/wezterm-mux-server
install -Dm755 target/release/strip-ansi-escapes %{buildroot}/usr/bin/strip-ansi-escapes


install -m644 assets/%{name}.desktop -pD %{buildroot}/usr/share/applications/org.wezfurlong.%{name}.desktop
install -m644 assets/icon/%{name}-icon.svg -pD %{buildroot}/usr/share/icons/hicolor/scalable/apps/org.wezfurlong.%{name}.svg
install -m644 assets/shell-integration/* -pD %{buildroot}/etc/profile.d
install -m644 assets/%{name}-nautilus.py -pD %{buildroot}/usr/share/nautilus-python/extensions/%{name}-nautilus.py

install -m644 assets/shell-completion/fish -pD %{buildroot}/usr/share/fish/vendor_completions.d/wezterm.fish
install -m644 assets/shell-completion/fish -pD %{buildroot}/usr/share/fish/vendor_completions.d/wezterm-gui.fish

install -m644 assets/shell-completion/bash -pD %{buildroot}/usr/share/bash-completion/completions/wezterm
install -m644 assets/shell-completion/bash -pD %{buildroot}/usr/share/bash-completion/completions/wezterm-gui

install -m644 assets/shell-completion/zsh -pD %{buildroot}/usr/share/zsh/site-functions/_wezterm
install -m644 assets/shell-completion/zsh -pD %{buildroot}/usr/share/zsh/site-functions/_wezterm-gui

%files
%defattr(-,root,root,-)
/usr/bin/wezterm
/usr/bin/wezterm-gui
/usr/bin/strip-ansi-escapes
/usr/bin/wezterm-mux-server
/usr/share/applications/org.wezfurlong.wezterm.desktop
/usr/share/icons/hicolor/scalable/apps/org.wezfurlong.wezterm.svg
/usr/share/nautilus-python/extensions/wezterm-nautilus.py
/usr/share/bash-completion
/usr/share/fish
/usr/share/zsh
