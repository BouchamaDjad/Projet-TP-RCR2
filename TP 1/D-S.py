from pyds import MassFunction

A =  "Oil Rig"
B =  "Cargo Ship"
C =  "Pipeline Lea"

# Definition des fonctions de masse
m1 = MassFunction({(A,): 0.7, (B,): 0.2, (A,B,C): 0.1})
m2 = MassFunction({(C,): 0.8, (A,B,C): 0.2})
m3 = MassFunction({(B,): 0.6, (A,B,C): 0.4})

# Combinaison des fonctions de masse
combined_m = m1 & m2 & m3

print('Combined mass function:\n', "\n".join([f"{c} : {v:.3f}" for c,v in combined_m.items()]), "\n")

hyp_sout = max(list(combined_m.items()), key=lambda x:x[1])

print("hypothese soutenu : (", hyp_sout[0], f", {hyp_sout[1]:.4f})\n")

confidence_intervale_length = dict([(h, combined_m.pl(h) - combined_m.bel(h)) for h in list(combined_m.keys())])

print('taille des intervalles de confiance : \n', "\n".join([f"{c} : {v:.3f}" for c,v in confidence_intervale_length.items()]), "\n")