from flask import Flask,request,jsonify
import pandas as pd
import pickle


app = Flask(__name__)

@app.route('/prediction',methods=['GET','POST'])
def home():
    # getting the available symptoms for input modification
    availablesymptoms=['itching' ,'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing',
 'shivering', 'chills' ,'joint_pain' ,'stomach_pain' ,'acidity',
 'ulcers_on_tongue' ,'muscle_wasting' ,'vomiting' ,'burning_micturition',
 'spotting_ urination' ,'fatigue' ,'weight_gain' ,'anxiety',
 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness',
 'lethargy' ,'patches_in_throat' ,'irregular_sugar_level' ,'cough',
 'high_fever', 'sunken_eyes', 'breathlessness' ,'sweating' ,'dehydration',
 'indigestion' ,'headache' ,'yellowish_skin' ,'dark_urine' ,'nausea',
 'loss_of_appetite', 'pain_behind_the_eyes' ,'back_pain' ,'constipation',
 'abdominal_pain' ,'diarrhoea' ,'mild_fever' ,'yellow_urine',
 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload',
 'swelling_of_stomach' ,'swelled_lymph_nodes' ,'malaise',
 'blurred_and_distorted_vision' ,'phlegm', 'throat_irritation',
 'redness_of_eyes' ,'sinus_pressure' ,'runny_nose' ,'congestion' ,'chest_pain',
 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements',
 'pain_in_anal_region' ,'bloody_stool' ,'irritation_in_anus' ,'neck_pain',
 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
 'swollen_blood_vessels' ,'puffy_face_and_eyes' ,'enlarged_thyroid',
 'brittle_nails' ,'swollen_extremeties', 'excessive_hunger',
 'extra_marital_contacts' ,'drying_and_tingling_lips' ,'slurred_speech',
 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck',
 'swelling_joints' ,'movement_stiffness' ,'spinning_movements',
 'loss_of_balance' ,'unsteadiness', 'weakness_of_one_body_side',
 'loss_of_smell' ,'bladder_discomfort' ,'foul_smell_of urine',
 'continuous_feel_of_urine' ,'passage_of_gases', 'internal_itching',
 'toxic_look_(typhos)' ,'depression' ,'irritability' ,'muscle_pain',
 'altered_sensorium' ,'red_spots_over_body' ,'belly_pain',
 'abnormal_menstruation' ,'dischromic _patches' ,'watering_from_eyes',
 'increased_appetite' ,'polyuria', 'family_history', 'mucoid_sputum',
 'rusty_sputum' ,'lack_of_concentration' ,'visual_disturbances',
 'receiving_blood_transfusion' ,'receiving_unsterile_injections' ,'coma',
 'stomach_bleeding' ,'distention_of_abdomen',
 'history_of_alcohol_consumption' ,'fluid_overload.1', 'blood_in_sputum',
 'prominent_veins_on_calf' ,'palpitations' ,'painful_walking',
 'pus_filled_pimples' ,'blackheads' ,'scurring' ,'skin_peeling',
 'silver_like_dusting' ,'small_dents_in_nails' ,'inflammatory_nails',
 'blister' ,'red_sore_around_nose' ,'yellow_crust_ooze' ,'chest_pain.1',
 'feeling_of_fullness_on_chest' ,'shortness_of_breath' ,'nausea.1',
 'arm_weakness', 'dizziness.1' ,'loss_of_vision', 'severe_headache',
 'bleeding' ,'coughing__blood' ,'chronic_cough' ,'pneumonia' ,'wheezing',
 'constipation.1' ,'diarrohea' ,'heart_burn', 'acid_reflux', 'vomiting_blood',
 'painful_urination' ,'blood_in_urine' ,'jaundice' ,'  muscle_pain',
 'swelling of body', 'inflammation', 'anexity', 'depression.1',
 'felling tense' ,'nightmares' ,'disinterest_in_regular_activities',
 'high fever' ,'suicidal_thoughts' ,'hallucinations' ,'delusions',
 'vomiting.1' ,'thirst_dehydration' ,'extreme_fatigue' ,'fainting',
 'chicken_pox' ,'  flu' ,'abdominal_pain.1', 'obesity.1', 'joint_pain.1',
 'shivering.1' ,'stomach_pain.1' ,'acidity.1' ,'skin rash',
 'internal bleeding', 'lethargy.1', 'weight loss', 'cramps.1', 'neck pain',
 'knee pain' ,'restlessness.1' ,'scurring.1' ,'back_pain.1' ,'neck_pain.1',
 'sweating.1' ,'low_blood_pressure', 'low_sugar_level' ,'high_blood_pressure',
 'high_sugar_level' ,'blurred_vision' ,'muscle_stiffness' ,'body_aches',
 'decreased_appetite', 'muscle_cramps' ,'aches_or_pains in bones',
 'excessive_sweating' ,'aggression' ,'agitation' ,'anxiety.1',
 'bad_taste_in_mouth' ,'bloating' ,'blackouts' ,'blinking_eyes', 'nervousness',
 'reduce in drinking water and eating food' ,'confusion' ,'mood_swings.1',
 'allergy', 'ankle_pain', 'poor_concentration' ,'sore_throat', 'bleeding_gums',
 'fainting.1' ,'frequent_squinting' ,'cold_hands' ,'excessive_crying',
 'nasal_congestion' ,'dry_eyes', 'hoarse_voice' ,'bad_taste' ,'cold_feet',
 'decreased_appetite.1' ,'difficulty_swallowing' ,'bad_breathe' ,'gum_sores',
 'spots_on_tonsils' ,'Lumps' ,'increased_thirst' ,'throat block',
 'sore_tongue' ,'swollen_tongue' ,'stomach_upset' ,'white_patches_on_tongue',
 'dry_mouth' ,'dry_eyes.1', 'feeling_faint' ,'noisy_breathing', 'mouth_sores',
 'enlarged_glands' ,'belching' ,'swelling in ankles' ,'skin_bumps' ,'red skin',
 'blue_colored_skin', 'morning_joint_stiffness', 'shaking_hands', 'red_eyes',
 'hoarse_voice.1' ,'hearing_loss' ,'learning_disability' ,'eye_irritation',
 'distended_stomach', 'difficulty_urinating', 'menstrual_bleeding',
 'Swollen lips', 'bruising.1', 'red_spots' ,'hoarseness' ,'neck_pain.2',
 'trouble_breathing', 'rashes', 'chills.1' ,'nose_bleed' ,'palpitations.1',
 'trembling' ,'stomach_cramps' ,'rapid_heart_rate' ,'tingling lips' ,'gagging',
 'cloudy_odor_urine', 'vaginal_dryness', 'vaginal_odor', 'itching.1',
 'irregular_periods' ,'vaginal_discharge' ,'no_menstrual_periods',
 'missed_periods' ,'coated_tongue' ,'mucus running from the nose',
 'kidney_failure' ,'food_poisoning' ,'discolouration_of_nail',
 'pain_in_centre_of_abdomen', 'stress' ,'nose_bleeding',
 'not_able_to_lift_both_arms' ,'face_dropped_on_one_side', 'paralysis',
 'severe pain in abdomin' ,'execessive bleeding' ,'feeling tired',
 'breath less' ,'pale skin', 'night sweats' ,'swollen glands', 'purple rashes',
 'repeated infections' ,'sickness' ,'Gallstones' ,'exhasustion',
 'sweling in tummy' ,'passing blood in stools', 'hair loss',
 'blotchy red palms' ,'increased sensitivity' ,'rectal bleeding',
 'pain in anus' ,'Lumps in sexual reproduction parts', ' mucus discharge',
 'bowel incontinence' ,'Swollen eyes' ,'swollen feet' ,'unconsciousness',
 'swelling in hips' ,'swelling in ribs' ,'swelling in knees',
 'osteoporosis (weakening of the bones)' ,'heart failure' ,'kidney disease',
 'inferiority', 'sense of dread' ,'irritation', 'concentration lack',
 'flushed face' ,'loss cartilage' ,'vaginal bleeding',
 'Stopping and Starting of urine' ,'frequent urination',
 'eating faster than normal' ,'eat large number of food' ,'painful periods',
 'burning sensation while urinating', 'pelvic pain', 'swelling legs',
 'very lethargic' ,'breething fast' ,'abnormal cold body' ,'convulsion',
 'swelling bones' ,'rapid bone breaking', 'Brain shutdown', 'death',
 'drowsiness' ,'seizures(fits)' ,'Change in size and shape of breasts',
 'discharge of blood in either of ur nipples', 'Swelling in arm pits',
 'change in appearance of nipples' ,'Blood stain in the phelm' ,'Migrane',
 'Running/blocked nose', 'bingeing', 'purging', 'focus on food',
 'swelling in kidney' ,'difficulty in walking' ,'arthritis in big toe',
 'blocked nose' ,'swollen skin', 'hot skin', 'persistent cough',
 'rapid heart beat' ,'clusters on body' ,'red patches with scratching',
 'stinging' ,'Bloating' ,'Blisters/Sore', 'skin swelling' ,'Sleep disturbance',
 'lack of memory power', 'swollen ankles' ,'diabetis',
 'dark and tarry stools' ,'IBS', 'getting older', 'wheat intollerance',
 'sneezing' ,'Angina' ,'continuous cough' ,'loss of smell' ,'loss of taste']
    # end 
    print(len(availablesymptoms))#debugging

    packet = {'response':'error','input':''}

    # getting the user symptom input 
    """
    user input model: <json> {"symptoms":list<string>}
    """
    userinput = request.get_json()
    userinput = userinput["symptoms"]
    userinput = userinput.split(',')
    userinput = [i.lower() for i in userinput]
    # end

    # preprocessing the input symptoms 
   ''' userinputlist = list(map(int,list('0'*len(availablesymptoms))))
    for i in range(len(availablesymptoms)):
        current = ' '.join(availablesymptoms[i].split('_')).lower()
        if current in userinput:
            userinputlist[i]=1
    packet['input']=' '.join(userinput) # debug
    # end

    # loading model and predicting
    model = pickle.load(open('disease_preditcor.pkl','rb'))
    prediction = model.predict([userinputlist])
    packet['response'] = prediction[0]
    # end'''
    
    return jsonify(packet)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
