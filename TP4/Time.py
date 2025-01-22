import subprocess
import numpy as np
import re

Nodes=[5,10,20,30]
Parents=[1,2,3,4,5]

def extract_and_convert_durations(text):
    inference_pattern = r"durée de l'inférence est:\s*([\d.]+)\s*millisecondes"
    propagation_pattern = r"temps de propagation\s*([\d.]+)\s*secondes"
    
    inference_match = re.search(inference_pattern, text)
    inference_duration = int(inference_match.group(1)) if inference_match else 0
    
    propagation_match = re.search(propagation_pattern, text)
    propagation_duration = float(propagation_match.group(1)) if propagation_match else 0
    
    return {
        "duree_de_inference": inference_duration,
        "temps_de_propagation": propagation_duration
    }

with open("time.csv", "w") as f:
    f.write("N,Parent_max,Passage(s),inference(ms)\n")
    
    for N in Nodes:
        for Parent in Parents:
            passages = []
            inferences = []
            
            f.write(f"{N},{Parent},")

            result = subprocess.run(["matlab","-nodesktop","-nosplash", "-batch",f"prop2evid({str(N)}, {str(Parent)})"], text=True, stderr=subprocess.PIPE)
            if result.returncode != 0:
                print(result.stderr)

            for _ in range(10):
                result = subprocess.run(["./passage.exe"], stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE)
                
                if result.returncode != 0:
                    print(result.stderr)
                    continue

                result = subprocess.run(["./inference.exe"], stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE)    
                
                if result.returncode != 0:
                    print(result.stderr)
                    continue

                resultats = open('resultats', 'r')
                durations = extract_and_convert_durations(resultats.read())

                if durations["duree_de_inference"]:
                    inferences.append(durations["duree_de_inference"])

                if durations["temps_de_propagation"]:
                    passages.append(durations["temps_de_propagation"])
            
            if passages != []:
                f.write(f"{np.mean(passages):.3f},")
            else:
                f.write("0,")

            if inferences != []:
                f.write(f"{np.mean(inferences)}\n")
            else:
                f.write("0\n")