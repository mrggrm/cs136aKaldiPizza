import os, sys, re

srcdir = "./dataset/dict"
dir = "./data/dict"
srcdict = srcdir + "/sw-ms98-dict_patched.text"
os .system ("mkdir -p " + dir)
with open (srcdict, "r") as f, open (dir + "/lexicon0.txt", 'w') as g:
  g .write (f .read () .upper ())
os .system ("awk '" + r'BEGIN{getline}($0 !~ /^#/) {print}' + "' " + dir + "/lexicon0.txt | sort | awk '" + r'($0 !~ /^[[:space:]]*$/) {print}' + "' > " + dir + "/lexicon1.txt || exit 1;")
with open (dir + "/lexicon1.txt", 'r') as f:
  with open (dir + "/nonsilence_phones.txt", 'w') as p:
    for phone in set ((re .sub (r'\n.*? ', ' ', f .read ())) .split () [1:]):
      p .write (phone + "\n")
with open (dir + "/silence_phones.txt", 'w') as f:
  for nsp in ['sil', 'spn', 'nsn', 'lau']:
    f .write (nsp + "\n")
with open (dir + "/optional_silence.txt", 'w') as f:
  f .write ("sil")
with open (dir + "/extra_questions.txt", 'w') as g:
  g .write ("-n")

with open (srcdir + "/MSU_single_letter.txt", 'r') as f:
  with open (dir + "/lexicon1.txt", 'r') as g:
    with open (dir + "/lexicon2.txt", 'w') as h:
      for line in ['!sil sil', '[vocalized-noise] spn', '[noise] nsn', \
                   '[laughter] lau', '<unk> spn']:
        h .write (line + "\n")
      h .write (f .read () .upper ())
      lexicon = re .sub (r'\[LAUGHTER-(.*?)\]', r'\1', g .read ())
      lexicon = re .sub (r'\[(.*?)/.*?\]', r'\1', lexicon)
      lexicon = re .sub (r'\[.*?\]|_[0-9]*|[\{\}]', r'', lexicon)
      h .write (lexicon)

os .system ("python format_acronyms_dict.py -i " + dir + "/lexicon2.txt -o " +\
  dir + "/lexicon3.txt -L " + srcdir + "/MSU_single_letter.txt -M " + dir + "/acronyms_raw.map")
os. system ("cat " + dir + "/acronyms_raw.map | sort -u > " + dir + "/acronyms.map")
os .system ("( echo 'i ay' )| cat - " + dir + "/lexicon3.txt | tr '[A-Z]' '[a-z]' | sort -u > " + dir + "/lexicon.txt")
os .system ("pushd " + dir + " >&/dev/null")
os .system ("popd >&/dev/null")
os .system ("rm " + dir + "/lexicon0.txt")
os .system ("rm " + dir + "/lexicon1.txt")
os .system ("rm " + dir + "/lexicon2.txt")
os .system ("rm " + dir + "/lexicon3.txt")
