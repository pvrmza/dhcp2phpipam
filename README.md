# dhcp2phpipam
Report isc-dhcp events to phpIPAM through its API



# in dhcpd.conf
on commit {
  set noname = concat("dhcp-", binary-to-ascii(10, 8, "-", leased-address));
  set ClientIP = binary-to-ascii(10, 8, ".", leased-address);
  set ClientDHCID = binary-to-ascii(16, 8, ":", substring(hardware, 1, 6));
  set ClientName = pick-first-value(option host-name, config-option-host-name, client-name, noname);
  set RouterIP = pick-first-value(binary-to-ascii(10, 8, ".", packet(24, 4)),none);

  log(concat("Commit: IP: ", ClientIP, " DHCID: ", ClientDHCID, " Name: ", RouterIP));

  execute("/usr/local/bin/dhcp2phpipm.py", "add", ClientIP, ClientDHCID, ClientName, RouterIP );
}

on release {
  set ClientIP = binary-to-ascii(10, 8, ".", leased-address);
  set ClientDHCID = binary-to-ascii(16, 8, ":", hardware);
  log(concat("Release: IP: ", ClientIP));
  execute("/usr/local/bin/dhcp2phpipm.py", "add", ClientIP, ClientDHCID);
}

on expiry {
  set ClientIP = binary-to-ascii(10, 8, ".", leased-address);
  log(concat("Expired: IP: ", ClientIP));
  execute("/usr/local/bin/dhcp2phpipm.py", "delete", ClientIP, "0", "0");
}
