import ipaddress
import optparse


parser = optparse.OptionParser(
    usage="Usage: %prog [OPTION]...<Input text_file name>...",
    description="Verify overlap of each IPv4 network in a spreadsheet column of multiple spreadsheets.\nIP-address or full CIDR syntax is needed: x.x.x.x/y, only one per cell.",
    epilog="Open Source MIT License. Written by Muhammed Jimoh",
)
parser.add_option(
    "-s",
    "--stats",
    action="store_true",
    help="Show stats on how many unique IP addresses found.",
)
parser.add_option(
    "-r",
    "--read-only",
    action="store_true",
    default=False,
    help="Open spreadsheets as read-only",
)
(ops, args) = parser.parse_args()


def open_file(args: str) -> str:
    file = open(args[0], "rb")
    ip_addresses = file.readlines()
    return ip_addresses


def process_ip_addresses(ip_addresses: str) -> list:
    nets = []
    no_intersection = []
    for i, row in enumerate(ip_addresses):
        row = (
            row.decode("utf-8").strip().split(",")
        )  # decode the byte object to obtain strings
        for val in row:
            try:
                ip = ipaddress.ip_network(val.replace(" ", ""))
                print(ip)
            except ValueError as err:
                print(
                    "Fatal:  value '%s' is not recognised as a IPv4 net."
                    % (val)
                )
                continue
            for net in nets:
                overlap = False
                if net.overlaps(ip):
                    overlap = True
                    print("  %s -> %s  overlaps" % (ip, net))
                    break
                # elif not overlap:
                no_intersection.append(str(ip))
            nets.append(ip)
    no_intersection = sorted(list(set(no_intersection)))
    return no_intersection


def no_of_intersections(no_intersection: list) -> list:
    ip_list = []
    for i in range(1, len(no_intersection), 2):
        ip_list.append((no_intersection[i - 1], no_intersection[i]))
    return ip_list


def write_to_output(ip_list: list) -> None:
    with open("output/output.txt", "w") as fp:
        for val in ip_list:
            fp.write(str(val).replace("'", "").strip("(").strip(")"))
            fp.writelines("\n")


def main() -> None:
    if len(args) == 0:
        parser.error("At least one text or .txt file is required!")

    ip_addresses = open_file(args)

    no_intersection_result = process_ip_addresses(ip_addresses=ip_addresses)

    processed_data = no_of_intersections(
        no_intersection=no_intersection_result
    )

    write_to_output(ip_list=processed_data)

    message = "\nSuccessfully processed the IP Adresses!"

    print(message)


if __name__ == "__main__":
    main()
