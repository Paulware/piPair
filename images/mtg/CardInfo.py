class CardInfo():
   cards = { \
      'artifacts/The Machine.jpg':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 0}, \
      'artifacts/ak47.png':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 1}, \
      'artifacts/beeBeeBun.jpg':{'colorless': 6, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 2}, \
      'artifacts/bfg.jpg':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 3}, \
      'artifacts/blackerLotus.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 4}, \
      'artifacts/blurryBeeble.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 1, 'white': 0, 'green': 0, 'power': 1, 'toughness': 1, 'id': 5}, \
      'artifacts/captainAmericasShield.png':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 6}, \
      'artifacts/chaosConfetti.jpg':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 7}, \
      'artifacts/doItYourselfSeraph.png':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 0, 'white': 2, 'green': 0, 'power': 4, 'toughness': 4, 'id': 8}, \
      'artifacts/doge.jpg':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 0, 'toughness': 1, 'id': 9}, \
      'artifacts/dragonBalls.jpg':{'colorless': 7, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 10}, \
      'artifacts/eagleFiveWinnebago.jpg':{'colorless': 6, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 4, 'toughness': 4, 'id': 11}, \
      'artifacts/fluxCapacitor.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 12}, \
      'artifacts/fodderCannon.jpg':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 13}, \
      'artifacts/galactus.jpg':{'colorless': 10, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 14}, \
      'artifacts/gatlingGun.png':{'kick': 1, 'colorless': 1, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 15}, \
      'artifacts/infinityGauntlet.png':{'colorless': 6, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 16}, \
      'artifacts/letterBomb.jpg':{'colorless': 6, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 17}, \
      'artifacts/limbReplacement.png':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 18}, \
      'artifacts/m1911.png':{'colorless': 9, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 19}, \
      'artifacts/molotov.png':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 20}, \
      'artifacts/nullRod.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 21}, \
      'artifacts/peeweesBike.jpg':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 22}, \
      'artifacts/predatorTech.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 23}, \
      'artifacts/psychicPaper.jpg':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 24}, \
      'artifacts/ratchetBomb.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 25}, \
      'artifacts/sonicScrewdriver.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 26}, \
      'artifacts/staffofdomination.jpg':{'colorless': 3, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 27}, \
      'artifacts/swordOfDungeonsAndDragons.jpg':{'colorless': 3, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 28}, \
      'artifacts/tardis.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 6, 'white': 0, 'green': 0, 'id': 29}, \
      'artifacts/tesseract.png':{'colorless': 3, 'red': 0, 'black': 0, 'blue': 1, 'white': 0, 'green': 0, 'id': 30}, \
      'artifacts/thatAss.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 31}, \
      'artifacts/tigerTank.png':{'colorless': 8, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 9, 'toughness': 9, 'id': 32}, \
      'artifacts/tinman.png':{'colorless': 3, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 1, 'toughness': 2, 'id': 33}, \
      'artifacts/urzasContactLenses.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 34}, \
      'creatures/agentSmith.jpg':{'power': 6, 'toughness': 6, 'colorless': 4, 'red': 0, 'black': 2, 'blue': 0, 'white': 0, 'green': 0, 'id': 35}, \
      'creatures/alGore.jpg':{'power': 1, 'toughness': 1, 'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 2, 'id': 36}, \
      'creatures/americanEagle.jpg':{'flying': True, 'power': 2, 'toughness': 2, 'colorless': 3, 'red': 1, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'id': 37}, \
      'creatures/android17.png':{'power': 2, 'toughness': 2, 'colorless': 2, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 38}, \
      'creatures/android18.png':{'power': 2, 'toughness': 2, 'colorless': 2, 'red': 1, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'id': 39}, \
      'creatures/annoyingOrange.jpg':{'haste': True, 'power': 1, 'toughness': 1, 'colorless': 0, 'red': 1, 'black': 0, 'blue': 1, 'white': 0, 'green': 1, 'id': 40}, \
      'creatures/arrgh.jpg':{'haste': True, 'power': 5, 'toughness': 5, 'colorless': 0, 'red': 0, 'black': 3, 'blue': 0, 'white': 0, 'green': 0, 'id': 41}, \
      'creatures/arthurKingOfTheBritains.jpg':{'power': 4, 'toughness': 5, 'colorless': 3, 'red': 0, 'black': 0, 'blue': 0, 'white': 2, 'green': 0, 'id': 42}, \
      'creatures/barackHObama.jpg':{'power': 0, 'toughness': 6, 'colorless': 1, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 43}, \
      'creatures/barackObama.jpg':{'power': 3, 'toughness': 7, 'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'grnblu': 3, 'whtblu': 3, 'id': 44}, \
      'creatures/barackObamaII.jpg':{'power': 1, 'toughness': 1, 'colorless': 3, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'id': 45}, \
      'creatures/barfEagleFiveNavigator.jpg':{'power': 3, 'toughness': 4, 'colorless': 1, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 46}, \
      'creatures/batman.jpg':{'power': 5, 'toughness': 5, 'colorless': 3, 'red': 0, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'id': 47}, \
      'creatures/batmanII.jpg':{'power': 5, 'toughness': 4, 'colorless': 3, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'whtblk': 3, 'id': 48}, \
      'creatures/berneyStinson.jpg':{'power': 4, 'toughness': 1, 'colorless': 0, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 49}, \
      'creatures/bernieSanders.jpg':{'power': 5, 'toughness': 8, 'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 2, 'green': 0, 'id': 50}, \
      'creatures/bernieSandersII.jpg':{'haste': True, 'power': 20, 'toughness': 20, 'colorless': 0, 'red': 1, 'black': 1, 'blue': 1, 'white': 1, 'green': 1, 'id': 51}, \
      'creatures/bickeringGiant.jpg':{'power': 3, 'toughness': 3, 'colorless': 0, 'red': 1, 'black': 1, 'blue': 0, 'white': 0, 'green': 1, 'id': 52}, \
      'creatures/biffTannen.jpg':{'power': 5, 'toughness': 5, 'colorless': 4, 'red': 1, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'id': 53}, \
      'creatures/blackKnight.jpg':{'power': 0, 'toughness': 2, 'colorless': 1, 'red': 0, 'black': 2, 'blue': 0, 'white': 0, 'green': 0, 'id': 54}, \
      'creatures/borgCube.jpg':{'flying': True, 'power': 1, 'toughness': 1, 'colorless': 4, 'red': 0, 'black': 2, 'blue': 0, 'white': 0, 'green': 0, 'id': 55}, \
      'creatures/borgQueen.jpg':{'power': 5, 'toughness': 5, 'colorless': 0, 'red': 0, 'black': 3, 'blue': 3, 'white': 2, 'green': 0, 'id': 56}, \
      'creatures/bruceLee.jpg':{'power': 99, 'toughness': 99, 'colorless': 0, 'red': 1, 'black': 1, 'blue': 1, 'white': 1, 'green': 1, 'id': 57}, \
      'creatures/burninator.jpg':{'power': 9, 'toughness': 9, 'colorless': 9, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 58}, \
      'creatures/cantinaBand.jpg':{'power': 1, 'toughness': 1, 'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'id': 59}, \
      'creatures/captainAmerica.jfif':{'power': 2, 'toughness': 2, 'colorless': 2, 'red': 1, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'id': 60}, \
      'creatures/charlesXavier.jpg':{'power': 2, 'toughness': 4, 'colorless': 2, 'red': 0, 'black': 0, 'blue': 2, 'white': 1, 'green': 0, 'id': 61}, \
      'creatures/cheatyFace.jpg':{'flying': True, 'power': 2, 'toughness': 2, 'colorless': 0, 'red': 0, 'black': 0, 'blue': 2, 'white': 0, 'green': 0, 'id': 62}, \
      'creatures/chivalrousChevalier.jpg':{'flying': True, 'power': 3, 'toughness': 3, 'colorless': 4, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'id': 63}, \
      'creatures/chuckNorris.jpg':{'power': 99, 'toughness': 99, 'colorless': 9, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'id': 64}, \
      'creatures/conanTheBarbarian.png':{'power': 3, 'toughness': 3, 'colorless': 2, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 65}, \
      'creatures/conanTheLibrarian.png':{'power': 4, 'toughness': 5, 'colorless': 2, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 66}, \
      'creatures/countTyroneRugen.jpg':{'power': 3, 'toughness': 4, 'colorless': 0, 'red': 1, 'black': 2, 'blue': 0, 'white': 0, 'green': 0, 'id': 67}, \
      'creatures/cowardlyLion.png':{'power': 1, 'toughness': 5, 'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'id': 68}, \
      'creatures/daenerysStormborn.jpg':{'power': 2, 'toughness': 2, 'colorless': 1, 'red': 1, 'black': 1, 'blue': 0, 'white': 1, 'green': 1, 'id': 69}, \
      'creatures/darkHelmet.jpg':{'power': 4, 'toughness': 5, 'colorless': 3, 'red': 0, 'black': 2, 'blue': 1, 'white': 0, 'green': 0, 'id': 70}, \
      'creatures/darthSidious.jpg':{'power': 5, 'toughness': 5, 'colorless': 4, 'red': 1, 'black': 1, 'blue': 1, 'white': 0, 'green': 0, 'id': 71}, \
      'creatures/darthVader.jpg':{'colorless': 5, 'red': 0, 'black': 5, 'blue': 0, 'white': 0, 'green': 0, 'power': 13, 'toughness': 13, 'id': 72}, \
      'creatures/darylDixon.jpg':{'colorless': 0, 'red': 5, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 6, 'toughness': 6, 'id': 73}, \
      'creatures/deadPool.png':{'colorless': 2, 'red': 2, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'power': 10, 'toughness': 10, 'haste': True, 'id': 74}, \
      'creatures/deadPoolAgain.jpg':{'colorless': 3, 'red': 1, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'power': 3, 'toughness': 3, 'haste': True, 'id': 75}, \
      'creatures/deadPoolIII.png':{'colorless': 4, 'red': 1, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'power': 3, 'toughness': 3, 'id': 76}, \
      'creatures/deadpoolFairyPrincess.jpg':{'colorless': 1, 'red': 1, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'power': 3, 'toughness': 3, 'id': 77}, \
      'creatures/dickJones.png':{'colorless': 3, 'red': 0, 'black': 2, 'blue': 0, 'white': 0, 'green': 0, 'power': 7, 'toughness': 7, 'id': 78}, \
      'creatures/doctorEmmettBrown.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 2, 'white': 0, 'green': 0, 'power': 1, 'toughness': 3, 'id': 79}, \
      'creatures/donkeyKong.png':{'colorless': 5, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'power': 7, 'toughness': 6, 'id': 80}, \
      'creatures/drHouse.jpg':{'colorless': 5, 'red': 0, 'black': 0, 'blue': 0, 'white': 3, 'green': 0, 'power': 2, 'toughness': 8, 'id': 81}, \
      'creatures/drStrange.jpg':{'colorless': 1, 'red': 0, 'black': 1, 'blue': 1, 'white': 1, 'green': 0, 'power': 1, 'toughness': 4, 'flying': True, 'id': 82}, \
      'creatures/draxDestroyer.jpg':{'colorless': 4, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'blublk': 1, 'power': 6, 'toughness': 4, 'id': 83}, \
      'creatures/earlOfSquirrel.jpg':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 2, 'power': 4, 'toughness': 4, 'id': 84}, \
      'creatures/extremelySlowZombie.jpg':{'colorless': 1, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'power': 3, 'toughness': 3, 'id': 85}, \
      'creatures/fezzikTheKindlyGiant.jpg':{'colorless': 1, 'red': 1, 'black': 0, 'blue': 0, 'white': 1, 'green': 1, 'power': 5, 'toughness': 6, 'id': 86}, \
      'creatures/frieza.jpg':{'colorless': 0, 'red': 0, 'black': 2, 'blue': 1, 'white': 0, 'green': 0, 'power': 1, 'toughness': 2, 'flying': True, 'id': 87}, \
      'creatures/gameStoreEmployee.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 2, 'white': 0, 'green': 0, 'power': 2, 'toughness': 2, 'id': 88}, \
      'creatures/gamora.jpg':{'colorless': 0, 'red': 1, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'power': 3, 'toughness': 2, 'id': 89}, \
      'creatures/gandalf.png':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'power': 2, 'toughness': 4, 'id': 90}, \
      'creatures/generalGrievous.jpg':{'colorless': 0, 'red': 0, 'black': 1, 'blue': 1, 'white': 1, 'green': 0, 'power': 2, 'toughness': 2, 'id': 91}, \
      'creatures/georgeBushII.jpg':{'colorless': 0, 'red': 1, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'power': 1, 'toughness': 4, 'id': 92}, \
      'creatures/georgeMcfly.jpg':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'power': 1, 'toughness': 2, 'id': 93}, \
      'creatures/georgeWBush.jpg':{'colorless': 0, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 1, 'toughness': 1, 'id': 94}, \
      'creatures/gilligan.png':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 2, 'green': 0, 'power': 1, 'toughness': 2, 'id': 95}, \
      'creatures/god.png':{'colorless': 0, 'red': 1, 'black': 1, 'blue': 1, 'white': 1, 'green': 1, 'power': 11, 'toughness': 11, 'flying': True, 'id': 96}, \
      'creatures/godzilla.jpg':{'colorless': 5, 'red': 1, 'black': 0, 'blue': 1, 'white': 0, 'green': 1, 'power': 7, 'toughness': 6, 'id': 97}, \
      'creatures/gordonRamsey.jpg':{'colorless': 3, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 3, 'toughness': 2, 'id': 98}, \
      'creatures/groot.jpg':{'colorless': 3, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 2, 'power': 8, 'toughness': 8, 'id': 99}, \
      'creatures/hanSolo.jpg':{'colorless': 3, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'power': 4, 'toughness': 3, 'id': 100}, \
      'creatures/hangman.jpg':{'colorless': 0, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'power': 1, 'toughness': 1, 'id': 101}, \
      'creatures/hela.png':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'blkred': 1, 'power': 4, 'toughness': 5, 'id': 102}, \
      'creatures/hillaryClinton.jpeg':{'colorless': 2, 'red': 1, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'power': 4, 'toughness': 3, 'id': 103}, \
      'creatures/hirohito.png':{'colorless': 3, 'red': 1, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'power': 4, 'toughness': 3, 'id': 104}, \
      'creatures/hitler.jpg':{'colorless': 0, 'red': 0, 'black': 4, 'blue': 0, 'white': 0, 'green': 0, 'power': 4, 'toughness': 5, 'id': 105}, \
      'creatures/hulk.png':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 6, 'power': 6, 'toughness': 6, 'id': 106}, \
      'creatures/indianaJones.jpg':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'power': 1, 'toughness': 3, 'id': 107}, \
      'creatures/infinityElemental.jpg':{'colorless': 4, 'red': 3, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 99, 'toughness': 5, 'id': 108}, \
      'creatures/inigoMontoya.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'redwht': 2, 'power': 4, 'toughness': 4, 'id': 109}, \
      'creatures/inigoMontoyaII.jpg':{'colorless': 0, 'red': 1, 'black': 0, 'blue': 0, 'white': 1, 'green': 1, 'power': 4, 'toughness': 4, 'id': 110}, \
      'creatures/ironMan.png':{'colorless': 2, 'red': 2, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'power': 3, 'toughness': 6, 'flying': True, 'id': 111}, \
      'creatures/ironManII.jpg':{'colorless': 5, 'red': 1, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'power': 5, 'toughness': 7, 'flying': True, 'id': 112}, \
      'creatures/itThatGetsLeftHanging.jpg':{'colorless': 5, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 5, 'toughness': 4, 'id': 113}, \
      'creatures/jaceTheAsshole.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 1, 'white': 0, 'green': 0, 'power': 2, 'toughness': 2, 'id': 114}, \
      'creatures/jamesKirk.png':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'blured': 2, 'power': 3, 'toughness': 5, 'id': 115}, \
      'creatures/jangoFett.jpg':{'colorless': 2, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 2, 'toughness': 2, 'flying': True, 'haste': True, 'id': 116}, \
      'creatures/jeanGrey.jpg':{'colorless': 3, 'red': 1, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'power': 3, 'toughness': 4, 'id': 117}, \
      'creatures/johnLennon.jpg':{'colorless': 3, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'grnblu': 2, 'power': 7, 'toughness': 7, 'id': 118}, \
      'creatures/johnnyCash.jpg':{'colorless': 3, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'whtblk': 2, 'power': 7, 'toughness': 7, 'id': 119}, \
      'creatures/johnnyCombo.png':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 2, 'white': 0, 'green': 0, 'power': 1, 'toughness': 1, 'id': 120}, \
      'creatures/josefStalin.png':{'colorless': 8, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 2, 'toughness': 8, 'id': 121}, \
      'creatures/joshLane.jpg':{'colorless': 0, 'red': 1, 'black': 1, 'blue': 1, 'white': 1, 'green': 1, 'power': 4, 'toughness': 20, 'id': 122}, \
      'creatures/kanyeWest.png':{'colorless': 0, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'power': 1, 'toughness': 1, 'id': 123}, \
      'creatures/killerBunny.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'power': 0, 'toughness': 1, 'id': 124}, \
      'creatures/kingKong.jpg':{'colorless': 3, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'power': 4, 'toughness': 6, 'haste': True, 'id': 125}, \
      'creatures/kittyPryde.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'power': 2, 'toughness': 2, 'id': 126}, \
      'creatures/koolAidMan.jpg':{'colorless': 2, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 2, 'toughness': 2, 'haste': True, 'id': 127}, \
      'creatures/krillin.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'power': 1, 'toughness': 1, 'id': 128}, \
      'creatures/libyanTerrorists.jpg':{'colorless': 4, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 3, 'toughness': 3, 'id': 129}, \
      'creatures/logan.jpg':{'colorless': 3, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'redgrn': 2, 'power': 3, 'toughness': 4, 'id': 130}, \
      'creatures/lordVoldemort.jpg':{'colorless': 3, 'red': 0, 'black': 3, 'blue': 0, 'white': 0, 'green': 0, 'power': 6, 'toughness': 4, 'flying': True, 'id': 131}, \
      'creatures/magneto.jpg':{'colorless': 3, 'red': 1, 'black': 1, 'blue': 1, 'white': 0, 'green': 0, 'power': 4, 'toughness': 4, 'id': 132}, \
      'creatures/mario.jpg':{'colorless': 3, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 3, 'toughness': 3, 'id': 133}, \
      'creatures/martyMcFly.jpg':{'colorless': 2, 'red': 2, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'power': 3, 'toughness': 4, 'haste': True, 'id': 134}, \
      'creatures/masterChief.png':{'colorless': 2, 'red': 1, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'power': 3, 'toughness': 3, 'haste': True, 'id': 135}, \
      'creatures/memePirate.jpeg':{'colorless': 2, 'red': 1, 'black': 0, 'blue': 1, 'white': 0, 'green': 0, 'power': 3, 'toughness': 3, 'id': 136}, \
      'creatures/miracleMax.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'power': 1, 'toughness': 3, 'id': 137}, \
      'creatures/mrT.jpg':{'colorless': 4, 'red': 1, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'power': 5, 'toughness': 5, 'id': 138}, \
      'creatures/mrTII.jpg':{'colorless': 0, 'red': 1, 'black': 1, 'blue': 1, 'white': 1, 'green': 1, 'power': 99, 'toughness': 99, 'id': 139}, \
      'creatures/mtgPlayer.png':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 2, 'toughness': 2, 'id': 140}, \
      'creatures/mysterioIllusionist.png':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 3, 'white': 0, 'green': 0, 'power': 1, 'toughness': 3, 'id': 141}, \
      'creatures/mystique.jpg':{'colorless': 3, 'red': 0, 'black': 1, 'blue': 2, 'white': 0, 'green': 0, 'power': 3, 'toughness': 3, 'id': 142}, \
      'creatures/mythBusters.jpg':{'colorless': 3, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 6, 'toughness': 4, 'id': 143}, \
      'creatures/nerdyPlayer.jpeg':{'colorless': 3, 'red': 0, 'black': 2, 'blue': 0, 'white': 0, 'green': 0, 'power': 4, 'toughness': 6, 'id': 144}, \
      'creatures/noviceBountyHunter.jpg':{'colorless': 1, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 2, 'toughness': 1, 'id': 145}, \
      'creatures/obiWanKenobi.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 1, 'white': 1, 'green': 1, 'power': 5, 'toughness': 5, 'id': 146}, \
      'creatures/oldGuard.jpg':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'power': 2, 'toughness': 1, 'id': 147}, \
      'creatures/patton.png':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 2, 'green': 0, 'power': 2, 'toughness': 2, 'id': 148}, \
      'creatures/peeweeHerman.jpg':{'colorless': 1, 'red': 1, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'power': 1, 'toughness': 4, 'id': 149}, \
      'creatures/pepe.jpg':{'colorless': 0, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'power': 0, 'toughness': 1, 'id': 150}, \
      'creatures/pikachu.png':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'blured': 2, 'power': 1, 'toughness': 2, 'id': 151}, \
      'creatures/pizzaTheHutt.jpg':{'colorless': 3, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 1, 'power': 3, 'toughness': 5, 'id': 152}, \
      'creatures/predator.png':{'colorless': 4, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'power': 3, 'toughness': 3, 'id': 153}, \
      'creatures/princeHumperdinck.jpg':{'colorless': 3, 'red': 0, 'black': 2, 'blue': 0, 'white': 0, 'green': 0, 'power': 2, 'toughness': 5, 'id': 154}, \
      'creatures/princessButtercup.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 2, 'green': 2, 'power': 2, 'toughness': 6, 'id': 155}, \
      'creatures/princessLeia.jpg':{'colorless': 3, 'red': 0, 'black': 0, 'blue': 1, 'white': 1, 'green': 1, 'power': 2, 'toughness': 2, 'id': 156}, \
      'creatures/ragePlayer.jpeg':{'colorless': 0, 'red': 3, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 4, 'toughness': 1, 'id': 157}, \
      'creatures/raichu.jpg':{'colorless': 3, 'red': 1, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'power': 5, 'toughness': 3, 'haste': True, 'id': 158}, \
      'creatures/ralphNader.jpg':{'colorless': 0, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 1, 'power': 2, 'toughness': 2, 'id': 159}, \
      'creatures/redForman.jpg':{'colorless': 0, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 1, 'toughness': 2, 'id': 160}, \
      'creatures/rickGrimes.png':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 1, 'power': 2, 'toughness': 1, 'id': 161}, \
      'creatures/riddick.jfif':{'colorless': 2, 'red': 1, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'power': 4, 'toughness': 4, 'id': 162}, \
      'creatures/robocop.jpg':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'power': 4, 'toughness': 4, 'id': 163}, \
      'creatures/rocketRaccoon.jpg':{'colorless': 0, 'red': 1, 'black': 0, 'blue': 1, 'white': 0, 'green': 1, 'power': 2, 'toughness': 2, 'id': 164}, \
      'creatures/rocketTropper.jpg':{'colorless': 1, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 2, 'toughness': 2, 'id': 165}, \
      'creatures/rodentOfUnusualSize.jpg':{'colorless': 0, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'power': 1, 'toughness': 1, 'id': 166}, \
      'creatures/samuelJackson.jpg':{'colorless': 0, 'red': 1, 'black': 1, 'blue': 1, 'white': 1, 'green': 1, 'power': 99, 'toughness': 99, 'id': 167}, \
      'creatures/santaClaus.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 2, 'power': 3, 'toughness': 3, 'flying': True, 'id': 168}, \
      'creatures/scorpionKing.png':{'colorless': 3, 'red': 1, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'power': 6, 'toughness': 5, 'id': 169}, \
      'creatures/secretGamer.jpeg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 4, 'green': 0, 'power': 3, 'toughness': 3, 'id': 170}, \
      'creatures/seleneBloodDrainer.png':{'colorless': 3, 'red': 0, 'black': 1, 'blue': 1, 'white': 1, 'green': 0, 'power': 4, 'toughness': 4, 'flying': True, 'id': 171}, \
      'creatures/shermanTank.png':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 2, 'white': 0, 'green': 0, 'power': 3, 'toughness': 5, 'id': 172}, \
      'creatures/silverSurfer.png':{'colorless': 1, 'red': 1, 'black': 1, 'blue': 1, 'white': 1, 'green': 1, 'power': 7, 'toughness': 7, 'flying': True, 'id': 173}, \
      'creatures/sirBedevere.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'power': 1, 'toughness': 3, 'id': 174}, \
      'creatures/sirRobin.png':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'power': 2, 'toughness': 2, 'id': 175}, \
      'creatures/spaceMarineCaptain.png':{'colorless': 3, 'red': 1, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'power': 4, 'toughness': 3, 'id': 176}, \
      'creatures/spiderman.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'blured': 2, 'power': 4, 'toughness': 2, 'id': 177}, \
      'creatures/spidermanII.png':{'colorless': 3, 'red': 1, 'black': 0, 'blue': 1, 'white': 0, 'green': 0, 'power': 4, 'toughness': 4, 'id': 178}, \
      'creatures/spock.png':{'colorless': 2, 'red': 2, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'power': 4, 'toughness': 4, 'id': 179}, \
      'creatures/starLord.jpg':{'colorless': 2, 'red': 1, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'power': 4, 'toughness': 3, 'id': 180}, \
      'creatures/steveAustin.png':{'kick': 1, 'colorless': 0, 'red': 1, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'power': 5, 'toughness': 6, 'haste': True, 'id': 181}, \
      'creatures/stevenRogers.jpg':{'colorless': 1, 'red': 0, 'black': 1, 'blue': 0, 'white': 3, 'green': 0, 'power': 4, 'toughness': 4, 'id': 182}, \
      'creatures/superBattleDroid.jpg':{'colorless': 5, 'red': 0, 'black': 0, 'blue': 1, 'white': 0, 'green': 0, 'power': 4, 'toughness': 5, 'id': 183}, \
      'creatures/superman.jpg':{'colorless': 3, 'red': 0, 'black': 0, 'blue': 2, 'white': 0, 'green': 0, 'power': 3, 'toughness': 3, 'id': 184}, \
      'creatures/supermanII.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 4, 'green': 0, 'power': 6, 'toughness': 6, 'flying': True, 'haste': True, 'id': 185}, \
      'creatures/supermanIII.png':{'colorless': 5, 'red': 1, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'power': 1, 'toughness': 1, 'flying': True, 'haste': True, 'id': 186}, \
      'creatures/t34Tank.jpg':{'colorless': 2, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 3, 'toughness': 3, 'id': 187}, \
      'creatures/thanos.jpg':{'colorless': 5, 'red': 0, 'black': 2, 'blue': 0, 'white': 0, 'green': 0, 'power': 9, 'toughness': 9, 'id': 188}, \
      'creatures/theCollector.jpeg':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 2, 'power': 2, 'toughness': 3, 'id': 189}, \
      'creatures/theJoker.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'blkred': 4, 'power': 2, 'toughness': 4, 'id': 190}, \
      'creatures/theOracle.jpg':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 2, 'white': 0, 'green': 0, 'power': 0, 'toughness': 3, 'id': 191}, \
      'creatures/theSilence.jpg':{'colorless': 4, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'power': 3, 'toughness': 3, 'id': 192}, \
      'creatures/thor.jpg':{'colorless': 2, 'red': 1, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'power': 6, 'toughness': 6, 'flying': True, 'id': 193}, \
      'creatures/thorGodOfThunder.png':{'colorless': 6, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'blured': 2, 'power': 5, 'toughness': 5, 'flying': True, 'id': 194}, \
      'creatures/thorSonOfOdin.png':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 1, 'power': 5, 'toughness': 4, 'id': 195}, \
      'creatures/timmyPowerGamer.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 2, 'power': 1, 'toughness': 1, 'id': 196}, \
      'creatures/toughNerd.jpeg':{'colorless': 2, 'red': 3, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 3, 'toughness': 5, 'id': 197}, \
      'creatures/tournamentGrinder.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'spike': 2, 'power': 1, 'toughness': 1, 'id': 198}, \
      'creatures/tribble.png':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'power': 1, 'toughness': 1, 'id': 199}, \
      'creatures/trooperCommander.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'power': 3, 'toughness': 3, 'id': 200}, \
      'creatures/trump.jpg':{'colorless': 1, 'red': 1, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'power': 3, 'toughness': 5, 'id': 201}, \
      'creatures/unwillingVolunteer.jpg':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'power': 1, 'toughness': 2, 'id': 202}, \
      'creatures/vegeta.png':{'colorless': 0, 'red': 1, 'black': 1, 'blue': 0, 'white': 0, 'green': 1, 'power': 3, 'toughness': 3, 'flying': True, 'id': 203}, \
      'creatures/vespaDruishPrincess.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 2, 'power': 2, 'toughness': 3, 'id': 204}, \
      'creatures/vizziniSicilianMastermind.jpg':{'colorless': 0, 'red': 1, 'black': 1, 'blue': 1, 'white': 0, 'green': 0, 'power': 2, 'toughness': 4, 'id': 205}, \
      'creatures/vladimirPutin.jpg':{'colorless': 3, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 2, 'power': 4, 'toughness': 4, 'id': 206}, \
      'creatures/wallOfTrump.png':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 2, 'white': 2, 'green': 0, 'power': 0, 'toughness': 6, 'id': 207}, \
      'creatures/warriorBug.png':{'colorless': 1, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'power': 1, 'toughness': 1, 'id': 208}, \
      'creatures/weepingStatue.jpg':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'power': 3, 'toughness': 3, 'id': 209}, \
      'creatures/westleyMasterofEverything.jpg':{'colorless': 0, 'red': 1, 'black': 0, 'blue': 1, 'white': 0, 'green': 1, 'power': 4, 'toughness': 5, 'id': 210}, \
      'creatures/youngChild.jpeg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 2, 'green': 0, 'power': 1, 'toughness': 1, 'id': 211}, \
      'enchantments/achHansRun.jpg':{'colorless': 2, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 2, 'id': 212}, \
      'enchantments/animateLibrary.jpg':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 2, 'white': 0, 'green': 0, 'id': 213}, \
      'enchantments/blitzkrieg.jpg':{'colorless': 0, 'red': 2, 'black': 2, 'blue': 0, 'white': 0, 'green': 0, 'id': 214}, \
      'enchantments/charmSchool.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'id': 215}, \
      'enchantments/curseOfTheFirePenguin.jpg':{'colorless': 4, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 216}, \
      'enchantments/executiveOversight.png':{'colorless': 4, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'id': 217}, \
      'enchantments/forceMastery.jpg':{'colorless': 3, 'red': 2, 'black': 0, 'blue': 1, 'white': 1, 'green': 1, 'id': 218}, \
      'enchantments/hiddenProtocol.png':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 2, 'white': 0, 'green': 0, 'id': 219}, \
      'enchantments/imposingVisage.jpg':{'colorless': 0, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 220}, \
      'enchantments/jediMindTrick.png':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 2, 'id': 221}, \
      'enchantments/lethalResponse.png':{'colorless': 1, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 222}, \
      'enchantments/looseLips.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 1, 'white': 0, 'green': 0, 'id': 223}, \
      'enchantments/nameDropping.jpg':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'id': 224}, \
      'enchantments/oprahsKindness.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'id': 225}, \
      'enchantments/privateContract.jpg':{'colorless': 1, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'id': 226}, \
      'enchantments/redRibbonArmy.png':{'colorless': 3, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 227}, \
      'enchantments/stricklandsDiscipline.jpg':{'colorless': 0, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'id': 228}, \
      'enchantments/theCheeseStandsAlone.jpg':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 0, 'white': 2, 'green': 0, 'id': 229}, \
      'enchantments/totalBodyProsthesis.png':{'colorless': 8, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 230}, \
      'instants/Race.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'whtblk': 1, 'id': 231}, \
      'instants/aestheticConsultation.jpg':{'colorless': 0, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'id': 232}, \
      'instants/capitolOffense.png':{'colorless': 2, 'red': 0, 'black': 2, 'blue': 0, 'white': 0, 'green': 0, 'id': 233}, \
      'instants/counterSpell.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 2, 'white': 0, 'green': 0, 'id': 234}, \
      'instants/curseOfTheRetarded.jpg':{'colorless': 2, 'red': 0, 'black': 2, 'blue': 1, 'white': 0, 'green': 0, 'id': 235}, \
      'instants/darkRitual.jpg':{'colorless': 0, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'id': 236}, \
      'instants/duh.jpg':{'colorless': 0, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'id': 237}, \
      'instants/enchantmentUndertheSea.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 1, 'id': 238}, \
      'instants/forcePush.jpg':{'colorless': 3, 'red': 0, 'black': 0, 'blue': 1, 'white': 0, 'green': 0, 'id': 239}, \
      'instants/gameOver.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 240}, \
      'instants/getALife.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'id': 241}, \
      'instants/gigawattBolt.jpg':{'colorless': 2, 'red': 3, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 242}, \
      'instants/holyHandgrenade.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'id': 243}, \
      'instants/iocanePowder.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'id': 244}, \
      'instants/jediReflex.jpg':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'id': 245}, \
      'instants/justDesserts.jpg':{'colorless': 1, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 246}, \
      'instants/kanyeInterrup.jpg':{'colorless': 0, 'red': 0, 'black': 1, 'blue': 1, 'white': 0, 'green': 0, 'id': 247}, \
      'instants/molotov.png':{'colorless': 3, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 248}, \
      'instants/moreOrLess.png':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 1, 'white': 0, 'green': 0, 'id': 249}, \
      'instants/notToday.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 2, 'white': 0, 'green': 0, 'id': 250}, \
      'instants/rickRoll.jpg':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 1, 'white': 0, 'green': 0, 'id': 251}, \
      'instants/shotInTheArm.jpg':{'colorless': 0, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 252}, \
      'instants/subtleInnuendo.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 1, 'white': 0, 'green': 0, 'id': 253}, \
      'instants/sugarRush.png':{'colorless': 3, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'id': 254}, \
      'instants/swiftDeath.jpg':{'colorless': 1, 'red': 0, 'black': 1, 'blue': 1, 'white': 0, 'green': 0, 'id': 255}, \
      'instants/unplug.jpg':{'colorless': 0, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'id': 256}, \
      'instants/veryCrypticCommand.jpg':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 3, 'white': 0, 'green': 0, 'id': 257}, \
      'lands/Island.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 1, 'white': 0, 'green': 0, 'id': 258}, \
      'lands/cliffsOfInsanity.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'redwht': 1, 'id': 259}, \
      'lands/deathStar.jpg':{'chargeCounter': 1, 'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 260}, \
      'lands/fireSwamp.jpg':{'colorless': 0, 'red': 1, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'id': 261}, \
      'lands/forest.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'id': 262}, \
      'lands/mountain.jpg':{'colorless': 0, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 263}, \
      'lands/pitOfDespair.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'redgrn': 1, 'id': 264}, \
      'lands/plains.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 0, 'id': 265}, \
      'lands/swamp.jpg':{'colorless': 0, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'id': 266}, \
      'sorcery/Visage of the Dread Pirate.jpg':{'colorless': 0, 'red': 1, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'id': 267}, \
      'sorcery/assWhuppin.png':{'colorless': 1, 'red': 0, 'black': 1, 'blue': 0, 'white': 1, 'green': 0, 'id': 268}, \
      'sorcery/batheInDragonbreath.png':{'colorless': 2, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 269}, \
      'sorcery/combTheDesert.jpg':{'colorless': 2, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'id': 270}, \
      'sorcery/damnation.jpg':{'colorless': 2, 'red': 0, 'black': 2, 'blue': 0, 'white': 0, 'green': 0, 'id': 271}, \
      'sorcery/fiveFingerDiscount.jpg':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 2, 'white': 0, 'green': 0, 'id': 272}, \
      'sorcery/hotFix.png':{'colorless': 4, 'red': 0, 'black': 0, 'blue': 1, 'white': 1, 'green': 0, 'id': 273}, \
      'sorcery/iKnowKungFu.jpg':{'colorless': 3, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'id': 274}, \
      'sorcery/inspirationalHeadBump.jpg':{'colorless': 1, 'red': 1, 'black': 0, 'blue': 1, 'white': 0, 'green': 0, 'id': 275}, \
      'sorcery/lastOneStanding.jpg':{'colorless': 1, 'red': 1, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'id': 276}, \
      'sorcery/ludicrousSpeed.jpg':{'colorless': 1, 'red': 1, 'black': 0, 'blue': 1, 'white': 0, 'green': 0, 'id': 277}, \
      'sorcery/manureDump.jpg':{'colorless': 1, 'red': 1, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'id': 278}, \
      'sorcery/michaelBay.jpg':{'colorless': 1, 'red': 2, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 279}, \
      'sorcery/naturalSpring.jpg':{'colorless': 3, 'red': 1, 'black': 0, 'blue': 1, 'white': 0, 'green': 2, 'id': 280}, \
      'sorcery/order66.jpg':{'colorless': 7, 'red': 0, 'black': 2, 'blue': 0, 'white': 0, 'green': 0, 'id': 281}, \
      'sorcery/organHarvest.png':{'colorless': 0, 'red': 0, 'black': 1, 'blue': 0, 'white': 0, 'green': 0, 'id': 282}, \
      'sorcery/peasants.png':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 0, 'white': 1, 'green': 1, 'id': 283}, \
      'sorcery/ponder.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 1, 'white': 0, 'green': 0, 'id': 284}, \
      'sorcery/powerNap.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 3, 'white': 0, 'green': 0, 'id': 285}, \
      'sorcery/reallyEpicPunch.jpg':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'id': 286}, \
      'sorcery/riseOfTheDarkRealms.jpg':{'colorless': 7, 'red': 0, 'black': 2, 'blue': 0, 'white': 0, 'green': 0, 'id': 287}, \
      'sorcery/scoutThePerimeter.jpg':{'colorless': 2, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 1, 'id': 288}, \
      'sorcery/timeWalk.jpg':{'colorless': 1, 'red': 0, 'black': 0, 'blue': 1, 'white': 0, 'green': 0, 'id': 289}, \
      'mtg.jpg':{'colorless': 0, 'red': 0, 'black': 0, 'blue': 0, 'white': 0, 'green': 0, 'id': 290} \
}
   def idToName (self,id): 
      name = ''
      if id <= len(self.cards):
         name = list(self.cards)[id]
      print ( 'Got name: ' + name )
      return (name)
