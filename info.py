locations = { \
   'North Atlantic':{'adjacents':['Norwegian Sea', 'Irish Sea', 'Mid Atlantic'],'x':104,'y':236, 'owner':None,'landType':'sea','occupied':False}, \
   'Norwegian Sea':{'adjacents':['Barents Sea', 'North Sea'],'x':463,'y':140, 'owner':None,'landType':'sea','occupied':False}, \
   'Barents Sea':{'adjacents':['Norwegian Sea'],'x':840,'y':29, 'owner':None,'landType':'sea','occupied':False}, \
   'Norway':{'adjacents':['Norwegian Sea', 'Barents Sea', 'Sweden', 'Finland', 'St Petersburg (North Coast)', 'St Petersburg (South Coast)'],'x':546,'y':284, 'owner':None,'landType':'coast','occupied':False}, \
   'Sweden':{'adjacents':['Norway', 'Finland', 'Gulf of Bothnia', 'Baltic Sea', 'Skagerrak'],'x':604,'y':318, 'owner':None,'landType':'land','occupied':False}, \
   'Gulf of Bothnia':{'adjacents':['Sweden', 'Finland', 'Livonia', 'St Petersburg (South Coast)'],'x':666,'y':283, 'owner':None,'landType':'sea','occupied':False}, \
   'Finland':{'adjacents':['Gulf of Bothnia', 'Norway', 'Sweden', 'St Petersburg (South Coast)', 'St Petersburg (North Coast)'],'x':747,'y':242, 'owner':None,'landType':'coast','occupied':False}, \
   'St Petersburg (North Coast)':{'adjacents':['Barents Sea', 'Finland', 'Moscow'],'x':853,'y':212, 'owner':None,'landType':'coast','occupied':False}, \
   'St Petersburg (South Coast)':{'adjacents':['Gulf of Bothnia', 'Finland', 'Moscow', 'Livonia'],'x':795,'y':324, 'owner':None,'landType':'coast','occupied':False}, \
   'Clyde':{'adjacents':['Edinburgh', 'Liverpool', 'North Atlantic'],'x':318,'y':360, 'owner':None,'landType':'coast','occupied':False}, \
   'Edinburgh':{'adjacents':['Clyde', 'Yorkshire', 'Liverpool', 'North Sea', 'Norwegian Sea'],'x':340,'y':366, 'owner':None,'landType':'coast','occupied':False}, \
   'North Sea':{'adjacents':['Edinburgh', 'Yorkshire', 'London', 'Belgium', 'Holland', 'Denmark', 'Norway', 'English Channel', 'Helgeland', 'Skagerrak', 'Norwegian Sea'],'x':433,'y':385, 'owner':None,'landType':'sea','occupied':False}, \
   'Skagerrak':{'adjacents':['Norway', 'Sweden', 'Denmark', 'North Sea', 'Baltic Sea'],'x':537,'y':350, 'owner':None,'landType':'sea','occupied':False}, \
   'Denmark':{'adjacents':['Kiel', 'Helgeland Bight', 'North Sea', 'Baltic Sea', 'Skagerrak'],'x':533,'y':410, 'owner':None,'landType':'coast','occupied':False}, \
   'Baltic Sea':{'adjacents':['Skagerrak', 'Gulf of Bothnia', 'Denmark', 'Sweden', 'Livonia', 'Prussia', 'Berlin', 'Kiel'],'x':624,'y':427, 'owner':None,'landType':'sea','occupied':False}, \
   'Livonia':{'adjacents':['Moscow', 'Prussia', 'Warsaw', 'St Petersburg (North Coast)', 'St Petersburg (South Coast)', 'Gulf of Bothnia', 'Baltic Sea'],'x':744,'y':418, 'owner':None,'landType':'coast','occupied':False}, \
   'Moscow':{'adjacents':['Livonia', 'Warsaw', 'Ukraine', 'St Petersburg (North Coast)', 'St Petersburg (South Coast)', 'Stevastopol'],'x':920,'y':395, 'owner':None,'landType':'land','occupied':False}, \
   'Irish Sea':{'adjacents':['North Atlantic', 'Mid Atlantic', 'English Channel', 'Liverpool', 'Wales'],'x':239,'y':467, 'owner':None,'landType':'sea','occupied':False}, \
   'Wales':{'adjacents':['Liverpool', 'Yorkshire', 'London', 'Irish Sea', 'English Channel'],'x':320,'y':460, 'owner':None,'landType':'coast','occupied':False}, \
   'Liverpool':{'adjacents':['Clyde', 'Edinburgh', 'Yorkshire', 'London', 'Wales', 'North Atlantic', 'Irish Sea'],'x':330,'y':431, 'owner':None,'landType':'coast','occupied':False}, \
   'Yorkshire':{'adjacents':['Edinburgh', 'Liverpool', 'London', 'Wales', 'North Sea'],'x':356,'y':434, 'owner':None,'landType':'coast','occupied':False}, \
   'London':{'adjacents':['Yorkshire', 'Wales', 'North Sea', 'English Channel'],'x':350,'y':480, 'owner':None,'landType':'coast','occupied':False}, \
   'Helgeland Bight':{'adjacents':['Denmark', 'Kiel', 'Holland', 'North Sea'],'x':470,'y':444, 'owner':None,'landType':'sea','occupied':False}, \
   'Kiel':{'adjacents':['Denmark', 'Berlin', 'Munich', 'Ruhr', 'Holland', 'Helgeland Bight', 'Baltic Sea'],'x':500,'y':485, 'owner':None,'landType':'coast','occupied':False}, \
   'Berlin':{'adjacents':['Prussia', 'Silesia', 'Munich', 'Kiel', 'Baltic Sea'],'x':565,'y':510, 'owner':None,'landType':'coast','occupied':False}, \
   'Prussia':{'adjacents':['Livonia', 'Silesia', 'Warsaw', 'Berlin', 'Baltic Sea'],'x':630,'y':484, 'owner':'Germany','landType':'coast','occupied':False}, \
   'Warsaw':{'adjacents':['Prussia', 'Livonia', 'Moscow', 'Ukraine', 'Silesia', 'Galicia'],'x':686,'y':526, 'owner':None,'landType':'land','occupied':False}, \
   'Mid Atlantic':{'adjacents':['North Atlantic', 'Irish Sea', 'English Channel', 'West Mediterranean', 'Brest', 'Gascony', 'Spain', 'Portugal', 'North Africa'],'x':85,'y':580, 'owner':None,'landType':'sea','occupied':False}, \
   'English Channel':{'adjacents':['Irish Sea', 'Mid Atlantic', 'North Sea'],'x':310,'y':517, 'owner':None,'landType':'sea','occupied':False}, \
   'Belgium':{'adjacents':['English Channel', 'North Sea', 'Holland', 'Ruhr', 'Burgundy', 'Picardy'],'x':406,'y':523, 'owner':None,'landType':'coast','occupied':False}, \
   'Holland':{'adjacents':['Kiel', 'Ruhr', 'Belgium', 'Helgeland Bight', 'North Sea'],'x':439,'y':505, 'owner':None,'landType':'coast','occupied':False}, \
   'Ruhr':{'adjacents':['Kiel', 'Munich', 'Burgundy', 'Belgium', 'Holland'],'x':473,'y':543, 'owner':None,'landType':'land','occupied':False}, \
   'Munich':{'adjacents':['Burgundy', 'Ruhr', 'Kiel', 'Berlin', 'Silesia', 'Bohemia', 'Tyrolia'],'x':522,'y':591, 'owner':None,'landType':'land','occupied':False}, \
   'Bohemia':{'adjacents':['Silesia', 'Galicia', 'Vienna', 'Tyrolia', 'Munich'],'x':574,'y':573, 'owner':None,'landType':'land','occupied':False}, \
   'Silesia':{'adjacents':['Berlin', 'Prussia', 'Warsaw', 'Galicia', 'Bohemia', 'Munich'],'x':606,'y':533, 'owner':None,'landType':'land','occupied':False}, \
   'Galicia':{'adjacents':['Warsaw', 'Ukraine', 'Rumania', 'Budapest', 'Vienna', 'Bohemia', 'Silesia'],'x':727,'y':580, 'owner':None,'landType':'land','occupied':False}, \
   'Ukraine':{'adjacents':['Moscow', 'Stevastopol', 'Rumania', 'Galicia', 'Warsaw'],'x':826,'y':550, 'owner':None,'landType':'land','occupied':False}, \
   'Stevastopol':{'adjacents':['Moscow', 'Ukraine', 'Armenia', 'Rumania', 'Black Sea'],'x':1000,'y':570, 'owner':None,'landType':'coast','occupied':False}, \
   'Brest':{'adjacents':['Picardy', 'Paris', 'Gascony', 'English Channel', 'Mid Atlantic'],'x':288,'y':563, 'owner':'France','landType':'coast','occupied':True}, \
   'Paris':{'adjacents':['Picardy', 'Burgundy', 'Gascony', 'Brest'],'x':370,'y':580, 'owner':'France','landType':'land','occupied':True}, \
   'Picardy':{'adjacents':['Belgium', 'Burgundy', 'Paris', 'Bret', 'English Channel'],'x':374,'y':545, 'owner':None,'landType':'coast','occupied':False}, \
   'Burgundy':{'adjacents':['Belgium', 'Ruhr', 'Munich', 'Marseilles', 'Gascony', 'Paris', 'Picardy'],'x':400,'y':600, 'owner':None,'landType':'land','occupied':False}, \
   'Tyrolia':{'adjacents':['Munich', 'Bohemia', 'Venezia', 'Piemonte', 'Trieste'],'x':540,'y':648, 'owner':None,'landType':'land','occupied':False}, \
   'Vienna':{'adjacents':['Bohemia', 'Galicia', 'Budapest', 'Trieste', 'Tyrolia'],'x':620,'y':625, 'owner':'Austria','landType':'land','occupied':True}, \
   'Budapest':{'adjacents':['Galicia', 'Rumania', 'Serbia', 'Trieste', 'Vienna'],'x':672,'y':642, 'owner':'Austria','landType':'land','occupied':True}, \
   'Rumania':{'adjacents':['Ukraine', 'Stevastopol', 'Black Sea', 'Bulgaria (South Coast)', 'Bulgaria (East Coast)', 'Serbia', 'Galicia'],'x':797,'y':702, 'owner':None,'landType':'coast','occupied':False}, \
   'Black Sea':{'adjacents':['Stevastopol', 'Armenia', 'Ankara', 'Constantinople', 'Bulgaria (South Coast)', 'Bulgaria (East Coast)', 'Rumania'],'x':936,'y':719, 'owner':None,'landType':'sea','occupied':False}, \
   'Gascony':{'adjacents':['Brest', 'Paris', 'Burgundy', 'Spain', 'Marseilles', 'Mid Atlantic'],'x':322,'y':677, 'owner':None,'landType':'coast','occupied':False}, \
   'Marseilles':{'adjacents':['Burgundy', 'Piemonte', 'Gascony', 'Spain', 'Gulf of Lyon'],'x':400,'y':700, 'owner':'France','landType':'coast','occupied':True}, \
   'Piemonte':{'adjacents':['Tyrolia', 'Venezia', 'Tuscany', 'Marseilles', 'Gulf of Lyon'],'x':467,'y':684, 'owner':None,'landType':'coast','occupied':False}, \
   'Venezia':{'adjacents':['Tyrolia', 'Trieste', 'Piemonte', 'Tuscany', 'Roma', 'Apulia'],'x':535,'y':676, 'owner':None,'landType':'coast','occupied':False}, \
   'Trieste':{'adjacents':['Tyrolia', 'Vienna', 'Budapest', 'Serbia', 'Albania', 'Adriatic Sea', 'Venezia'],'x':601,'y':692, 'owner':'Austria','landType':'coast','occupied':True}, \
   'Serbia':{'adjacents':['Budapest', 'Bulgaria', 'Rumania', 'Greece', 'Albania', 'Trieste'],'x':683,'y':729, 'owner':None,'landType':'land','occupied':False}, \
   'Portugal':{'adjacents':['Spain', 'Mid Atlantic'],'x':118,'y':744, 'owner':None,'landType':'coast','occupied':False}, \
   'Spain (North Coast)':{'adjacents':['Portugal', 'Gascony', 'Marseilles', 'Mid Atlantic', 'Gulf of Lyon', 'West Mediterranean'],'x':240,'y':691, 'owner':None,'landType':'coast','occupied':False}, \
   'Spain (South Coast)':{'adjacents':['Portugal', 'Gascony', 'Marseilles', 'Mid Atlantic', 'Gulf of Lyon', 'West Mediterranean'],'x':254,'y':806, 'owner':None,'landType':'coast','occupied':False}, \
   'Gulf of Lyon':{'adjacents':['Spain (South Coast)', 'Marseilles', 'Piemonte', 'Tuscany', 'Tyrhennian Sea', 'West Mediterranean'],'x':404,'y':771, 'owner':None,'landType':'sea','occupied':False}, \
   'Tuscany':{'adjacents':['Piemonte', 'Venezia', 'Roma', 'Gulf of Lyon', 'Tyrhennian Sea'],'x':512,'y':736, 'owner':None,'landType':'coast','occupied':False}, \
   'Roma':{'adjacents':['Tuscany', 'Venezia', 'Apulia', 'Napoli', 'Tyrhennian Sea'],'x':542,'y':782, 'owner':None,'landType':'coast','occupied':False}, \
   'Apulia':{'adjacents':['Venezia', 'Napoli', 'Roma', 'Adriatic Sea', 'Ionian Sea'],'x':586,'y':792, 'owner':None,'landType':'coast','occupied':False}, \
   'Napoli':{'adjacents':['Roma', 'Apulia', 'Tyrhennian Sea', 'Ionian Sea'],'x':570,'y':809, 'owner':None,'landType':'coast','occupied':False}, \
   'Adriatic Sea':{'adjacents':['Venezia', 'Trieste', 'Albania', 'Apulia', 'Ionian Sea'],'x':593,'y':756, 'owner':None,'landType':'sea','occupied':False}, \
   'Albania':{'adjacents':['Trieste', 'Serbia', 'Greece', 'Adriatic Sea', 'Ionian Sea'],'x':675,'y':796, 'owner':None,'landType':'coast','occupied':False}, \
   'Bulgaria (East Coast)':{'adjacents':['Rumania', 'Constantinople', 'Serbia', 'Greece', 'Black Sea'],'x':810,'y':738, 'owner':None,'landType':'coast','occupied':False}, \
   'Bulgaria (South Coast)':{'adjacents':['Rumania', 'Constantinople', 'Serbia', 'Greece', 'Aegean Sea'],'x':776,'y':799, 'owner':None,'landType':'coast','occupied':False}, \
   'Constantinople':{'adjacents':['Bulgaria (South Coast)', 'Bulgaria (East Coast)', 'Ankara', 'Smyrna', 'Black Sea', 'Aegean Sea'],'x':839,'y':795, 'owner':None,'landType':'coast','occupied':False}, \
   'Ankara':{'adjacents':['Armenia', 'Smyrna', 'Constantinople', 'Black Sea'],'x':936,'y':800, 'owner':None,'landType':'coast','occupied':False}, \
   'Armenia':{'adjacents':['Stevastopol', 'Syria', 'Ankara', 'Smyrna', 'Black Sea'],'x':1102,'y':798, 'owner':None,'landType':'coast','occupied':False}, \
   'North Africa':{'adjacents':['Tunisia', 'Mid Atlantic', 'West Mediterranean'],'x':145,'y':913, 'owner':None,'landType':'coast','occupied':False}, \
   'West Mediterranean':{'adjacents':['Spain', 'North Africa', 'Tunisia', 'Mid Atlantic'],'x':316,'y':850, 'owner':None,'landType':'sea','occupied':False}, \
   'Tunisia':{'adjacents':['North Africa', 'West Mediterranean', 'Tyrhennian Sea', 'Ionian Sea'],'x':459,'y':920, 'owner':None,'landType':'coast','occupied':False}, \
   'Tyrhennian Sea':{'adjacents':['Tuscany', 'Roma', 'Napoli', 'Tunisia', 'Gulf of Lyon', 'West Mediterranean', 'Ionian Sea'],'x':504,'y':841, 'owner':None,'landType':'sea','occupied':False}, \
   'Ionian Sea':{'adjacents':['Napoli', 'Apulia', 'Greece', 'Tunisia', 'Tyrhennian Sea', 'Adriatic Sea', 'Aegean Sea'],'x':626,'y':930, 'owner':None,'landType':'sea','occupied':False}, \
   'Greece':{'adjacents':['Albania', 'Serbia', 'Bulgaria (South Coast)', 'Bulgaria (East Coast)', 'Aegean Sea', 'Ionian Sea', 'Adriatic Sea'],'x':720,'y':854, 'owner':None,'landType':'coast','occupied':False}, \
   'Aegean Sea':{'adjacents':['Greece', 'Bulgaria (South Coast)', 'Constantinople', 'Smyrna', 'East Mediterranean', 'Ionian Sea'],'x':785,'y':883, 'owner':None,'landType':'sea','occupied':False}, \
   'Smyrna':{'adjacents':['Constantinople', 'Ankara', 'Armenia', 'Syria', 'East Mediterranean', 'Aegean Sea'],'x':932,'y':863, 'owner':None,'landType':'coast','occupied':False}, \
   'East Mediterranean':{'adjacents':['Smyrna', 'Syria', 'Aegean Sea', 'Ionian Sea'],'x':873,'y':938, 'owner':None,'landType':'sea','occupied':False}, \
   'Syria':{'adjacents':['Armenia', 'Smyrna', 'East Mediterranean'],'x':1082,'y':896, 'owner':None,'landType':'coast','occupied':False}, \
}
