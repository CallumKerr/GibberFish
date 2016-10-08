encodedict = {}
decodedict = {y : x for x, y in encodedict.items()}
ascl = b'\x00\x09\x0a !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

if __name__ == "__main__":
	import argparse
	
	parser = argparse.ArgumentParser()
	parser.add_argument('infile', type=argparse.FileType("rb"), help='File to encode/decode, .txt/.gibf respectively.')
	parser.add_argument('outfile', type=argparse.FileType("x"), help='File to encode/decode to, .gibf/.txt respectively.')
	encordec = parser.add_mutually_exclusive_group(required=True)
	encordec.add_argument('-e', '--e', action = 'store_true')
	encordec.add_argument('-d', '--d', action = 'store_true')
	arguments = parser.parse_args()

	code = arguments.infile.read()
	code = code.replace(b'\r\n',b'\n').replace(b'\r',b'\n')

	if arguments.e:
		try:
			for i in code:
				if i in ascl:
					outfile.write(i)
				else:
					outfile.write(encodedict[i])
			print("Encode was completed successfully!")
		except KeyError:
			print("The {} character is not in the Gibberfish code page!".format(i))
		
	else:
		try:
			for i in codelist:
				if i in ascl:
					outfile.write(i)
				else:
					outfile.write(decodedict[i])
			print("Decode was completed successfully!")
		except KeyError:
			print("The hex value {:#04x} is not in the Gibberfish code page!".format(ord(i.decode())))
	
	infile.close()
	outfile.close()