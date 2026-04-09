import random
import pandas as pd

# read in PC details
pc_details = pd.read_csv('PC Macro Test.csv')
pc_details

# Create reference dictionaries
skill_stat_dict = {
    'Perception':'WIS',
    'Stealth':'DEX',
    'Deception':'CHA',
    'Arcana':'INT',
    'Nature': 'WIS',
    'Occultism': 'INT',
    'Religion': 'WIS',
    'Society': 'INT',
    'Lore_1': 'INT',
    'Lore_2': 'INT',
}

prof_score_dict = {
    'Untrained': 0,
    'Trained': 2,
    'Expert': 4,
    'Master': 6,
    'Legendary': 8,
}

pc_names = pc_details.PC.to_list()
stat_list = ['Level', 'STR', 'DEX', 'CON',
             'INT', 'WIS', 'CHA']
all_pc_stats = dict()
all_pc_skills = dict()

for name in pc_names:
    row = pc_details[pc_details['PC']==name].index[0]
    df = pc_details.iloc[row]
    
    pc_stats = dict()
    for stat in stat_list:
        pc_stats[stat] = int(df[stat])
    all_pc_stats[name] = pc_stats

    pc_skills = dict()
    for skill in skill_stat_dict:
        skill_str = df[skill]
        # clean string
        skill_num = skill_str.split()[0]
        # Lookup corresponding value
        skill_num = prof_score_dict[skill_num]
        # Add level if mimimum Trained
        if skill_num > 0:
            skill_num += all_pc_stats[name]['Level']
        # Add stat
        stat = skill_stat_dict[skill]
        skill_num += all_pc_stats[name][stat]
        # Calculate skill DC
        skill_dc = 10 + skill_num
        pc_skills[skill] = [skill_str, skill_dc, skill_num]
    all_pc_skills[name] = pc_skills
          



output_df = pd.DataFrame()
output_index = list()

for skill in skill_stat_dict:
    output_index.append(skill)
    output_index.append('DC')
    output_index.append('Roll')

output_df.index = output_index

for name in all_pc_skills:
    pc_col = list()
    for skill in skill_stat_dict:
        pc_skills = all_pc_skills[name]
        pc_col.append(pc_skills[skill][0])
        pc_col.append(pc_skills[skill][1])
        roll = random.randint(1, 20)
        if roll == 1:
            roll = str(pc_skills[skill][2] + roll) + ' Crit Fail'
        elif roll == 20:
            roll = str(pc_skills[skill][2] + roll) + ' Crit Success'
        else:
            roll = str(pc_skills[skill][2] + roll)
        pc_col.append(roll)
        

    output_df[name] = pc_col

display(output_df)