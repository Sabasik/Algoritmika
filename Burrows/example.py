from BWTs import BWTSuffixes, invertTransformFaster, BWTSuffixes2, BWTSuffixesIndexes, invertTransformFasterWindow, runBWTonFile, reverseBWTonFile

BWT = BWTSuffixesIndexes()
text = "AATCGCTAGGATCCTAATCGCTAGTCCG"
text = """Tõde ja õigus I


					A. H. Tammsaare



See oli läinud aastasaja kolmanda veerandi lõpul. Päike lähenes silmapiirile, seistes sedavõrd madalas, et enam ei ulatunud valgustama ei mäkke ronivat hobust, kes puutelgedega vankrit vedas, ei vankril istuvat noort naist ega ka ligi kolmekümnelist meest, kes kõndis vankri kõrval.

Varsti jõudsid teelised mäerinnakul nii kõrgele, et päikeses helendama lõid mehe nägu – laiavõitu, tugevate lõuapäradega, terassilmadega, lühikese, kuid tiheda musta habemega –, naise nukrad silmad, look ja hobuse kikkis kõrvadega pea.

„Seal ta ongi, see Vargamäe," lausus mees ja näitas käega üle soo järgmise väljamäe poole, kus lömitas rühm madalaid hooneid. „Meie hooned paistavad, teiste omad seisavad mäe taga orus, sellest siis rahva suus Mäe ja Oru, mõisakirjas aga Eespere ja Tagapere. Paremat kätt see männitukk seal kõrgel mäe otsas on meie oma: igavesed vanad jändrikud teised, mõned poolkuivad juba."

Nii palju tegi mees juttu, siis logises vanker endiselt tummas vaikuses.

Naine silmitses ümbrust: siin mägi, seal mägi, kaugemal kolmas, pahemat kätt neljas, paremat viies ja nende taga kuues, seitsmes ning veel rohkemgi. Mägedel põllud ja hooned, mägede ümber, nende vahel aina soo, tükati raba, kaetud kidura võserikuga.

Üks niisugune mäenukk teda ümbritseva soo ja mõne männijändrikuga mäe kõrgemal tipul saab tema, sõitva naise koduks ja seal peab ta vististi oma päevad lõpetama.

Millegipärast kiskus noore naise süda valusasti rinnas kokku. Valu ulatus nagu madalamalegi, tabas kogu elundite kava, mis oleks nagu naba ümber puntras.

Jah, kunagi polnud ta osanud arvata, et temal võiks kord niisugune kodu olla. Tänini oli ta kodu all mõistnud ikka põldu ja metsa – suurt laant, mis õhtuti heliseb, kui huigatakse või kui aetakse pasunat. Aga mis heliseks siin, kui tuleks lust lõõritada? Hüüavad siis sood vastu, hakkavad rabad rõkkama?

Naine vaatas meest, kes hobuse kõrval kõndis, vaatas hobust, keda ta isakodus oli näinud sündivat ja kasvavat, – mõlemad tõttasid täiel sammul, nagu ootaks neid õnn ees.

Ja äkki tuli talle meelde, kuidas kodus oli aru peetud, peab ta oma praeguse mehe kosjad vastu võtma või tagasi lükkama. Ja kõik – vanemad, vennad, õed – olid otsustanud: sellele mehele võib minna, tema jaksab ja oskab naist toita. Imelik oli tol korral tundunud, et räägiti tema toitmisest. Kas siis tema ise ei oska tööd teha, et end ise toita, nagu iga teinegi tervete ihuliikmetega inimene?

Uuesti vaadates, kui kähku mees ja hobu kõrvuti uue kodu poole astusid, muutus ka tema meel rahulikumaks, süda julgemaks. Peaasi, et mära, see nende majapidamise üks peatugesid ja põhivara – nagu isa hobust kaasavaraks andes oli öelnud –, peaasi, et tema nii tõttavalt astus. See andis ka noorele naisele usku ja lootust.

„Astu aga astu," sundis mees hobust, nagu aimaks ta naise mõtteid, „saame ehk päevaveeruks koju."

„Kas jõuame," kahtles naine. Ka tema oli mõelnud kuidagi sõna „kodu" tarvitada, aga sõna jäi kurku kinni.

Lausal väljamäel oli tee pisut siledam, sellepärast kargas mees naise kõrvale vankrile, kahmas ohjad pingutavalt pihku ja ajas hobuse sörkima. Millegipärast valdas hobust äkki mingisugune rõõmuhelk ja ta hirnatas.

„Tunneb kodu lähedust," arvas mees.

„Nojah, tema käib juba mitut-setut korda seda teed," lausus naine. Endal oli aga nagu valus, et hobune seda võõrast paika juba koduna tunneb. Hobuse rõõmuhirnatuses kustus nagu tükk naise senisest elust.

Natuke maad pahemat kätt teest kõrval asuva talu õuel seisis üksik naine ja vaatas möödasõitjaid, ämber käe otsas. Vargamäe Eespere noorele perenaisele näis seisja nii tuttavana, nagu oleks ta teda juba ammugi ja sagedasti näinud. Veel enam: nagu oleks ta ise kustuva päikese helgil nõnda kuskil taluõuel seisnud ja möödaminejaid vaadelnud ja nagu teeks ta seda ka tulevikus veel lugematuid kordi.

„Mis selle talu nimi on?" küsis naine."""
print(f'Input: {text}')
transformed = BWT.transformWindow(text, 100)
print(f'Transformed: {transformed}')
inverted = invertTransformFasterWindow(transformed, 100)
print(f'Inverted: {inverted}')
print(text == inverted)
print(len(text), len(transformed))
print()


