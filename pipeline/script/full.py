# -*- coding: utf-8 -*-
"""Full script: paired English / Tamil segments (same order, same count) grouped in chapters.
Run `python3 -I script/full.py` to write en_full.txt, ta_full.txt and chapters.json."""
import json, os

Y = {  # Tamil years in words
    1957: "ஆயிரத்து தொள்ளாயிரத்து ஐம்பத்தேழு", 1961: "ஆயிரத்து தொள்ளாயிரத்து அறுபத்தொன்று", 1962: "ஆயிரத்து தொள்ளாயிரத்து அறுபத்திரண்டு",
    1964: "ஆயிரத்து தொள்ளாயிரத்து அறுபத்துநான்கு", 1979: "ஆயிரத்து தொள்ளாயிரத்து எழுபத்தொன்பது", 1982: "ஆயிரத்து தொள்ளாயிரத்து எண்பத்திரண்டு",
    1985: "ஆயிரத்து தொள்ளாயிரத்து எண்பத்தைந்து", 1986: "ஆயிரத்து தொள்ளாயிரத்து எண்பத்தாறு", 1987: "ஆயிரத்து தொள்ளாயிரத்து எண்பத்தேழு",
    1988: "ஆயிரத்து தொள்ளாயிரத்து எண்பத்தெட்டு", 1989: "ஆயிரத்து தொள்ளாயிரத்து எண்பத்தொன்பது", 1990: "ஆயிரத்து தொள்ளாயிரத்து தொண்ணூறு",
    1991: "ஆயிரத்து தொள்ளாயிரத்து தொண்ணூற்றொன்று",
}

CHAPTERS = [
 dict(id="P", en="Prologue", ta="முன்னுரை", years=(1991, 1991), segs=[
  ("On the evening of the twenty-fifth of December, nineteen ninety-one, a red flag came down over the Kremlin.",
   "ஆயிரத்து தொள்ளாயிரத்து தொண்ணூற்றொன்றாம் ஆண்டு, டிசம்பர் இருபத்தைந்தாம் தேதி மாலை. கிரெம்ளின் மாளிகையின் மேல் பறந்த செங்கொடி, மெதுவாகக் கீழிறக்கப்பட்டது."),
  ("For almost seven decades, that flag had flown over one of the two most powerful nations on Earth. The Soviet Union stretched across eleven time zones, held fifteen republics, and was home to roughly two hundred and ninety million people.",
   "கிட்டத்தட்ட எழுபது ஆண்டுகளாக, உலகின் இரண்டு மாபெரும் வல்லரசுகளில் ஒன்றான சோவியத் ஒன்றியத்தின் அடையாளமாக அந்தக் கொடி பறந்தது. பதினொன்று நேர மண்டலங்களில் பரந்து விரிந்த அந்த நாட்டில், பதினைந்து குடியரசுகள் இருந்தன; ஏறக்குறைய இருபத்தொன்பது கோடி மக்கள் வாழ்ந்தார்கள்."),
  ("It had sent the first satellite, and the first human, into space. Its army faced the West across a divided Europe.",
   "உலகின் முதல் செயற்கைக்கோளையும், விண்வெளிக்குச் சென்ற முதல் மனிதனையும் அனுப்பியது அதுதான். பிளவுபட்ட ஐரோப்பாவில், மேற்கு நாடுகளை எதிர்த்து அதன் இராணுவம் நின்றது."),
  ("And yet, within a few months, it ceased to exist. No foreign army invaded. No bomb fell on Moscow.",
   "ஆனால், சில மாதங்களிலேயே அந்த நாடு இல்லாமல் போனது. எந்த அந்நிய இராணுவமும் படையெடுக்கவில்லை; மாஸ்கோ மீது ஒரு குண்டும் விழவில்லை."),
  ("So what happened? How does a superpower end, not with a bang, but with a signature? This is the story of how the Soviet Union fell: a stagnant economy, a costly war, a disaster at Chernobyl, and a leader who set out to reform the system, and set in motion forces he could not control.",
   "அப்படியானால், என்ன நடந்தது? ஒரு வல்லரசு எப்படி முடிவுக்கு வரும்? தேங்கிப்போன பொருளாதாரம், விலை உயர்ந்த ஒரு போர், செர்னோபில் பேரழிவு, அமைப்பைச் சீர்திருத்த முயன்று, தன்னால் கட்டுப்படுத்த முடியாத சக்திகளை விடுவித்த ஒரு தலைவர். இதுதான் சோவியத் ஒன்றியம் வீழ்ந்த கதை."),
 ]),
 dict(id="C1", en="The Giant", ta="பெருவல்லரசு", years=(1957, 1985), segs=[
  ("To understand why the Soviet Union fell, start with how strong it once looked. It rebuilt itself after the Second World War, built an atomic bomb, and in nineteen fifty-seven launched Sputnik, the first satellite in orbit. In nineteen sixty-one, Yuri Gagarin became the first human being in space.",
   f"சோவியத் ஒன்றியம் வீழ்ந்தது ஏன் என்று புரிந்துகொள்ள, அது ஒரு காலத்தில் எவ்வளவு வலிமையாகத் தோன்றியது என்பதிலிருந்து தொடங்க வேண்டும். இரண்டாம் உலகப் போருக்குப் பிறகு அது தன்னை மீண்டும் கட்டியெழுப்பியது; அணுகுண்டை உருவாக்கியது; {Y[1957]}-இல், ஸ்புட்னிக் என்ற முதல் செயற்கைக்கோளை விண்ணில் செலுத்தியது. {Y[1961]}-இல், யூரி ககாரின் விண்வெளிக்குச் சென்ற முதல் மனிதரானார்."),
  ("Its rivalry with the United States shaped the whole world. Both sides built thousands of nuclear weapons, backed opposing governments from Cuba to Vietnam, and in nineteen sixty-two came close to nuclear war over missiles in Cuba.",
   f"அமெரிக்காவுடனான போட்டி உலகம் முழுவதையும் பாதித்தது. இரு தரப்பும் ஆயிரக்கணக்கான அணு ஆயுதங்களைக் குவித்தன; கியூபா முதல் வியட்நாம் வரை எதிரெதிர் அரசுகளுக்கு ஆதரவளித்தன; {Y[1962]}-இல், கியூபாவில் ஏவுகணைகள் தொடர்பாக அணுப்போரின் விளிம்புக்கே வந்தன."),
  ("In Moscow, each May Day, columns of soldiers and missiles rolled across Red Square. From nineteen sixty-four, the man on the reviewing stand was Leonid Brezhnev, who sat down with American presidents as an equal. To the outside world, the Soviet Union looked like a permanent fixture.",
   f"ஒவ்வொரு மே தினத்திலும், மாஸ்கோவின் சிவப்பு சதுக்கத்தில் வீரர்களின் அணிவகுப்பும் ஏவுகணைகளும் ஊர்ந்து சென்றன. {Y[1964]}-இலிருந்து, அந்த மேடையில் நின்றவர் லியோனிட் பிரெஷ்நேவ்; அவர் அமெரிக்க அதிபர்களுடன் சமமாக அமர்ந்து பேசினார். வெளியுலகுக்கு, சோவியத் ஒன்றியம் என்றும் நிலைத்திருக்கும் ஒன்றாகவே தெரிந்தது."),
  ("At home, something was wrong. The planned economy that had once raced ahead was slowing down. Factories met their targets on paper, shops ran short of basic goods, and people stood in long queues. Reform was discussed, and then quietly put away.",
   "ஆனால் உள்ளே, ஏதோ தவறாக இருந்தது. ஒரு காலத்தில் வேகமாக வளர்ந்த திட்டமிட்ட பொருளாதாரம் மெதுவடைந்தது. தொழிற்சாலைகள் காகிதத்தில் இலக்குகளை எட்டின; கடைகளில் அடிப்படைப் பொருட்களுக்குப் பற்றாக்குறை; மக்கள் நீண்ட வரிசைகளில் காத்திருந்தனர். சீர்திருத்தம் பற்றிப் பேசப்பட்டது; பிறகு அமைதியாக ஒதுக்கி வைக்கப்பட்டது."),
  ("Brezhnev's long rule came to be called the era of stagnation. When he died in nineteen eighty-two, two elderly successors followed, and both died within about two years. Then, in March nineteen eighty-five, the Politburo chose a much younger man, fifty-four-year-old Mikhail Gorbachev.",
   f"பிரெஷ்நேவின் நீண்ட ஆட்சி, தேக்க காலம் என்று அழைக்கப்பட்டது. {Y[1982]}-இல் அவர் இறந்தபோது, முதிய தலைவர்கள் இருவர் அடுத்தடுத்து வந்து, இரண்டே ஆண்டுகளில் மறைந்தனர். பிறகு, {Y[1985]} மார்ச்சில், பொலிட்பீரோ மிகவும் இளையவரான ஐம்பத்துநான்கு வயது மிகைல் கோர்பச்சேவைத் தேர்ந்தெடுத்தது."),
 ]),
 dict(id="C2", en="A New Leader", ta="ஒரு புதிய தலைவர்", years=(1985, 1987), segs=[
  ("Gorbachev knew that the system was in trouble. He did not want to destroy it; he wanted to save it. His plan came down to two Russian words that the world would soon learn. Perestroika meant restructuring: loosening the grip of central planning, and letting enterprises make some of their own decisions.",
   "சோவியத் அமைப்பு சிக்கலில் இருப்பதை கோர்பச்சேவ் அறிந்திருந்தார். அதை அழிக்க அவர் விரும்பவில்லை; காப்பாற்றவே விரும்பினார். அவரது திட்டம் இரண்டு ரஷ்யச் சொற்களில் அடங்கியது. பெரெஸ்ட்ரோயிகா என்றால் மறுசீரமைப்பு; மத்தியத் திட்டமிடலின் பிடியைத் தளர்த்தி, நிறுவனங்கள் சில முடிவுகளைத் தாமே எடுக்க விடுவது."),
  ("Glasnost meant openness. Newspapers began to report problems that had long been hidden. Banned books were published. Citizens could criticise their leaders in public for the first time in decades, and many political prisoners were released.",
   "கிளாஸ்நோஸ்ட் என்றால் வெளிப்படைத்தன்மை. நீண்ட காலம் மறைக்கப்பட்ட பிரச்சினைகளை நாளிதழ்கள் வெளியிடத் தொடங்கின. தடை செய்யப்பட்ட நூல்கள் வெளிவந்தன. பல ஆண்டுகளுக்குப் பிறகு முதல்முறையாக, மக்கள் தலைவர்களை வெளிப்படையாக விமர்சிக்க முடிந்தது; பல அரசியல் கைதிகள் விடுவிக்கப்பட்டனர்."),
  ("Abroad, Gorbachev changed the tone just as much. He met Ronald Reagan in Geneva and in Reykjavik, and in December nineteen eighty-seven they signed the INF Treaty in Washington, the first agreement to eliminate a whole class of nuclear missiles. The arms race, which was swallowing Soviet resources, began to slow.",
   f"வெளிநாட்டிலும் கோர்பச்சேவ் சூழ்நிலையை மாற்றினார். ஜெனீவாவிலும் ரெய்க்யாவிக்கிலும் ரொனால்ட் ரீகனைச் சந்தித்தார்; {Y[1987]} டிசம்பரில், வாஷிங்டனில், ஒரு முழு வகை அணு ஏவுகணைகளையே அழிக்கும் முதல் ஒப்பந்தத்தில் இருவரும் கையெழுத்திட்டனர். சோவியத் வளங்களை விழுங்கிக்கொண்டிருந்த ஆயுதப் போட்டி மெதுவடையத் தொடங்கியது."),
  ("In the West, Gorbachev became a celebrity. But reform has a way of releasing forces that its author cannot control, and inside the Soviet Union, the results were very different.",
   "மேற்குலகில் கோர்பச்சேவ் பிரபலமானார். ஆனால் சீர்திருத்தம், அதைத் தொடங்கியவரால் கட்டுப்படுத்த முடியாத சக்திகளை விடுவித்துவிடும். சோவியத் ஒன்றியத்துக்குள் விளைவுகள் முற்றிலும் வேறாக இருந்தன."),
 ]),
 dict(id="C3", en="An Economy in Trouble", ta="தடுமாறும் பொருளாதாரம்", years=(1985, 1989), segs=[
  ("The Soviet economy was planned by officials. Prices were fixed, factories received quotas, and a huge share of resources went to the military. It could build rockets and tanks, but it struggled to make good consumer goods, and it fell further behind the West in computers and technology.",
   "சோவியத் பொருளாதாரம் அதிகாரிகளால் திட்டமிடப்பட்டது. விலைகள் நிர்ணயிக்கப்பட்டன; தொழிற்சாலைகளுக்கு இலக்குகள் வழங்கப்பட்டன; வளங்களில் பெரும்பகுதி இராணுவத்துக்குச் சென்றது. அது ராக்கெட்டுகளையும் டாங்கிகளையும் உருவாக்க முடிந்தது; ஆனால் நல்ல நுகர்வுப் பொருட்களைத் தயாரிக்கத் திணறியது; கணினிகளிலும் தொழில்நுட்பத்திலும் மேற்கைவிடப் பின்தங்கியது."),
  ("One thing held it together: oil. Oil and gas brought in most of the hard currency the country used to buy grain and machinery from abroad. Then, in nineteen eighty-six, the price of oil collapsed, from about twenty-seven dollars a barrel the year before to about fourteen.",
   f"ஒன்று மட்டுமே அதைத் தாங்கி நின்றது: எண்ணெய். தானியங்களையும் இயந்திரங்களையும் வெளிநாடுகளில் வாங்கப் பயன்படுத்திய அந்நியச் செலாவணியில் பெரும்பகுதியை எண்ணெயும் எரிவாயுவும் தந்தன. பிறகு, {Y[1986]}-இல், எண்ணெய் விலை சரிந்தது; முந்தைய ஆண்டு ஏறத்தாழ இருபத்தேழு டாலராக இருந்த ஒரு பீப்பாய், சுமார் பதினான்கு டாலருக்கு வந்தது."),
  ("The country's income shrank just as it was trying to reform. Shortages grew worse, the budget deficit widened, and the new rules often made things more chaotic, not less. In some cities, ration coupons returned for goods like sugar and soap.",
   "சீர்திருத்தம் செய்ய முயன்ற அதே நேரத்தில் நாட்டின் வருமானம் சுருங்கியது. பற்றாக்குறை மோசமானது; பட்ஜெட் பற்றாக்குறை விரிவடைந்தது; புதிய விதிகள் பல நேரம் குழப்பத்தையே கூட்டின. சில நகரங்களில், சர்க்கரை, சோப்பு போன்ற பொருட்களுக்கு ரேஷன் சீட்டுகள் மீண்டும் வந்தன."),
  ("By the end of the decade, empty shelves had become part of daily life. And people could now say so out loud. Openness had given them the freedom to complain.",
   "பத்தாண்டின் இறுதியில், காலியான அலமாரிகள் அன்றாட வாழ்வின் பகுதியாகிவிட்டன. இப்போது மக்கள் அதை வாய்விட்டுச் சொல்லவும் முடிந்தது. வெளிப்படைத்தன்மை அவர்களுக்குக் குறை சொல்லும் சுதந்திரத்தைத் தந்திருந்தது."),
 ]),
 dict(id="C4", en="The War", ta="முடிவில்லாத போர்", years=(1979, 1989), segs=[
  ("There was also a war that would not end. In December nineteen seventy-nine, Soviet troops entered Afghanistan to prop up a friendly government. They expected a short operation.",
   f"முடிவே இல்லாத ஒரு போரும் இருந்தது. {Y[1979]} டிசம்பரில், நட்பு அரசைத் தாங்கிப் பிடிக்க, சோவியத் படைகள் ஆப்கானிஸ்தானுக்குள் நுழைந்தன. அது ஒரு குறுகிய நடவடிக்கை என்று அவர்கள் நினைத்தனர்."),
  ("Instead, they met a determined insurgency, backed with weapons and money from abroad, in mountains where tanks were of little use. The war dragged on for nine years. Roughly fifteen thousand Soviet soldiers were killed, and Afghan casualties were far higher.",
   "ஆனால் அவர்கள் எதிர்கொண்டது, வெளிநாட்டு ஆயுதங்களாலும் பணத்தாலும் ஆதரிக்கப்பட்ட உறுதியான கிளர்ச்சி; டாங்கிகள் அதிகம் பயன்படாத மலைகளில். போர் ஒன்பது ஆண்டுகள் இழுத்தது. ஏறத்தாழ பதினைந்தாயிரம் சோவியத் வீரர்கள் கொல்லப்பட்டனர்; ஆப்கானியர்களின் இழப்பு அதைவிட மிக அதிகம்."),
  ("Gorbachev called it a bleeding wound. The last Soviet troops crossed the border in February nineteen eighty-nine, without anything resembling the victory they had been promised. The war had cost lives, money and, above all, public trust.",
   f"கோர்பச்சேவ் அதை இரத்தம் வடியும் புண் என்றார். {Y[1989]} பிப்ரவரியில், கடைசி சோவியத் வீரர்கள் எல்லையைக் கடந்தனர்; வாக்களிக்கப்பட்ட வெற்றி எதுவும் இல்லாமல். அந்தப் போர் உயிர்களையும் பணத்தையும், எல்லாவற்றுக்கும் மேலாக, மக்களின் நம்பிக்கையையும் விலையாகப் பெற்றது."),
 ]),
 dict(id="C5", en="Chernobyl", ta="செர்னோபில்", years=(1986, 1986), segs=[
  ("On the twenty-sixth of April nineteen eighty-six, during a safety test, reactor number four at the Chernobyl nuclear power plant in Ukraine exploded. A fire burned for days and sent radioactive material high into the atmosphere.",
   f"{Y[1986]} ஏப்ரல் இருபத்தாறாம் தேதி, ஒரு பாதுகாப்புச் சோதனையின் போது, உக்ரைனில் உள்ள செர்னோபில் அணுமின் நிலையத்தின் நான்காம் உலை வெடித்தது. தீ பல நாட்கள் எரிந்து, கதிரியக்கப் பொருட்களை வளிமண்டலத்தின் உயரத்துக்கு அனுப்பியது."),
  ("For two days the Soviet public was told almost nothing. It was radiation alarms in Sweden that alerted the world. Tens of thousands of people were evacuated from the nearby town of Pripyat, and hundreds of thousands more were eventually resettled. Firefighters, soldiers and miners worked on the site, many of them paying with their health.",
   "இரண்டு நாட்கள் சோவியத் மக்களுக்கு எதுவுமே சொல்லப்படவில்லை. ஸ்வீடனில் ஒலித்த கதிர்வீச்சு எச்சரிக்கைகளே உலகை எச்சரித்தன. அருகிலுள்ள பிரிப்யாத் நகரிலிருந்து பல்லாயிரம் பேர் வெளியேற்றப்பட்டனர்; பின்னர் இன்னும் பல நூறாயிரம் பேர் இடம் மாற்றப்பட்டனர். தீயணைப்பு வீரர்களும் படைவீரர்களும் சுரங்கத் தொழிலாளர்களும் அங்கே உழைத்தனர்; பலர் தங்கள் உடல்நலத்தையே விலையாகக் கொடுத்தனர்."),
  ("Chernobyl showed how much the system hid, and how little citizens could trust it. Gorbachev himself later suggested that it may have been the real turning point, more than any reform. The cleanup cost the state enormous sums at the worst possible moment.",
   "அமைப்பு எவ்வளவு மறைத்தது, மக்கள் அதை எவ்வளவு குறைவாக நம்பினார்கள் என்பதை செர்னோபில் காட்டியது. எந்தச் சீர்திருத்தத்தையும்விட அதுவே உண்மையான திருப்புமுனையாக இருந்திருக்கலாம் என்று கோர்பச்சேவே பின்னர் கூறினார். மிக மோசமான நேரத்தில், அந்தத் துப்புரவுப் பணிக்கு அரசு பெரும் தொகையைச் செலவிட வேண்டியிருந்தது."),
 ]),
 dict(id="C6", en="Forces Unleashed", ta="விடுபட்ட சக்திகள்", years=(1988, 1991), segs=[
  ("The first cracks appeared in the Caucasus. In February nineteen eighty-eight, Armenians in Nagorno-Karabakh, a region inside Azerbaijan, demanded to join Armenia, and violence between the two peoples followed. A state built to deny such conflicts could not resolve it.",
   f"முதல் விரிசல்கள் காக்கசஸில் தோன்றின. {Y[1988]} பிப்ரவரியில், அசர்பைஜானுக்குள் உள்ள நகோர்னோ-கரபாக் பகுதியின் ஆர்மீனியர்கள், ஆர்மீனியாவுடன் இணைய வேண்டும் என்று கோரினர்; இரு இனங்களுக்கிடையே வன்முறை வெடித்தது. அத்தகைய மோதல்களை மறுக்கவே கட்டப்பட்ட ஓர் அரசால் அதைத் தீர்க்க முடியவில்லை."),
  ("As glasnost spread, people across the fifteen republics began to talk about what had long been suppressed: language, history, identity. In the Baltic states, activists revealed the secret deal of nineteen thirty-nine, the Molotov–Ribbentrop Pact, that had led to their annexation by the Soviet Union.",
   "கிளாஸ்நோஸ்ட் பரவ, பதினைந்து குடியரசுகளிலும் மக்கள், நீண்ட காலம் ஒடுக்கப்பட்டவற்றைப் பற்றிப் பேசத் தொடங்கினர்: மொழி, வரலாறு, அடையாளம். பால்டிக் நாடுகளில், ஆயிரத்து தொள்ளாயிரத்து முப்பத்தொன்பதாம் ஆண்டின் மொலோட்டோவ்–ரிப்பன்ட்ரோப் ஒப்பந்தம் என்ற ரகசிய உடன்படிக்கை, தங்கள் நாடுகள் சோவியத் ஒன்றியத்துடன் இணைக்கப்படக் காரணமானது என்பதை செயல்பாட்டாளர்கள் வெளிப்படுத்தினர்."),
  ("On the twenty-third of August nineteen eighty-nine, the fiftieth anniversary of that pact, about two million people joined hands in a human chain across Estonia, Latvia and Lithuania, roughly six hundred and seventy-five kilometres long. It was called the Baltic Way. It was peaceful, and impossible to ignore.",
   f"{Y[1989]} ஆகஸ்ட் இருபத்துமூன்றாம் தேதி, அந்த ஒப்பந்தத்தின் ஐம்பதாம் ஆண்டு நினைவு நாளில், எஸ்தோனியா, லாத்வியா, லிதுவேனியா வழியாக ஏறத்தாழ இருபது லட்சம் மக்கள் கைகோர்த்து, சுமார் அறுநூற்று எழுபத்தைந்து கிலோமீட்டர் நீளமான மனிதச் சங்கிலி அமைத்தனர். அதற்குப் பால்டிக் பாதை என்று பெயர். அது அமைதியானது; புறக்கணிக்க முடியாதது."),
  ("Elsewhere, protest was met with force. Soviet troops killed demonstrators in Tbilisi, in Georgia, in April nineteen eighty-nine, and in Vilnius, in January nineteen ninety-one. Each time, Gorbachev's reputation suffered, and the movements grew. Nationalism, once hidden under one flag, was becoming the strongest political force in the country.",
   f"வேறு இடங்களில், போராட்டங்கள் படைபலத்தால் எதிர்கொள்ளப்பட்டன. ஜார்ஜியாவின் திபிலிசியில் {Y[1989]} ஏப்ரலிலும், வில்னியசில் {Y[1991]} ஜனவரியிலும் சோவியத் படைகள் போராட்டக்காரர்களைக் கொன்றன. ஒவ்வொரு முறையும் கோர்பச்சேவின் நற்பெயர் சரிந்தது; இயக்கங்கள் வளர்ந்தன. ஒரே கொடியின் கீழ் மறைந்திருந்த தேசியவாதம், நாட்டின் வலிமையான அரசியல் சக்தியாக மாறிக்கொண்டிருந்தது."),
 ]),
 dict(id="C7", en="The Year Everything Changed", ta="எல்லாம் மாறிய ஆண்டு", years=(1989, 1989), segs=[
  ("Meanwhile, Eastern Europe was watching. Gorbachev had made it clear that Moscow would no longer send tanks to prop up unpopular governments. In Poland, the trade union Solidarity won partly free elections in June nineteen eighty-nine. In Hungary, the border with Austria was opened.",
   f"இதற்கிடையே கிழக்கு ஐரோப்பா கவனித்துக்கொண்டிருந்தது. மக்கள் ஆதரவற்ற அரசுகளைத் தாங்கிப் பிடிக்க இனி மாஸ்கோ டாங்கிகளை அனுப்பாது என்பதை கோர்பச்சேவ் தெளிவுபடுத்தியிருந்தார். போலந்தில், சாலிடாரிட்டி தொழிற்சங்கம், {Y[1989]} ஜூனில், பகுதியளவு சுதந்திரத் தேர்தலில் வென்றது. ஹங்கேரியில், ஆஸ்திரியாவுடனான எல்லை திறக்கப்பட்டது."),
  ("Then, on the ninth of November nineteen eighty-nine, East Germany announced that its citizens could cross to the West. Crowds gathered at the Berlin Wall, the guards stepped aside, and people climbed it, danced on it, and began to tear it down. The wall that had divided Europe for twenty-eight years was suddenly open.",
   f"பிறகு, {Y[1989]} நவம்பர் ஒன்பதாம் தேதி, கிழக்கு ஜெர்மனி தன் குடிமக்கள் மேற்குக்குச் செல்லலாம் என்று அறிவித்தது. பெர்லின் சுவரில் மக்கள் திரண்டனர்; காவலர்கள் விலகி நின்றனர்; மக்கள் அதன் மேல் ஏறி, நடனமாடி, இடிக்கத் தொடங்கினர். இருபத்தெட்டு ஆண்டுகள் ஐரோப்பாவைப் பிரித்த சுவர் திடீரெனத் திறந்தது."),
  ("Within weeks, communist governments fell in Czechoslovakia and Bulgaria, and by Christmas, in Romania. The order that Soviet power had held in place for forty years came apart in a single year, almost without Soviet force.",
   "சில வாரங்களுக்குள், செக்கோஸ்லோவாக்கியாவிலும் பல்கேரியாவிலும் கம்யூனிச அரசுகள் வீழ்ந்தன; கிறிஸ்துமஸுக்குள் ருமேனியாவிலும். நாற்பது ஆண்டுகளாக சோவியத் வலிமை தாங்கிப் பிடித்த அந்த ஒழுங்கு, ஓராண்டில், கிட்டத்தட்ட சோவியத் படைபலமே இல்லாமல் சிதறியது."),
 ]),
 dict(id="C8", en="Two Leaders", ta="இரு தலைவர்கள்", years=(1990, 1991), segs=[
  ("At home, politics had changed too. In March nineteen ninety, the Communist Party gave up its constitutional monopoly on power, and Gorbachev became the first, and only, president of the Soviet Union. But a rival was rising.",
   f"உள்நாட்டிலும் அரசியல் மாறியிருந்தது. {Y[1990]} மார்ச்சில், அதிகாரத்தின்மேல் இருந்த அரசியலமைப்பு ஏகபோகத்தை கம்யூனிஸ்ட் கட்சி கைவிட்டது; கோர்பச்சேவ் சோவியத் ஒன்றியத்தின் முதல், ஒரே அதிபரானார். ஆனால் ஒரு போட்டியாளர் எழுந்துகொண்டிருந்தார்."),
  ("Boris Yeltsin, a former party chief in Moscow, had been pushed out by Gorbachev, and returned as a champion of Russia itself. In June nineteen ninety, Russia declared its sovereignty. A year later, Yeltsin was elected President of Russia by popular vote. Now Moscow had two centres of power: the Soviet Union's, and Russia's.",
   f"மாஸ்கோவின் முன்னாள் கட்சித் தலைவரான போரிஸ் யெல்ட்சினை கோர்பச்சேவ் ஒதுக்கியிருந்தார்; அவர் ரஷ்யாவின் காவலராகத் திரும்பி வந்தார். {Y[1990]} ஜூனில், ரஷ்யா தன் இறையாண்மையை அறிவித்தது. ஓராண்டு கழித்து, யெல்ட்சின் மக்கள் வாக்கால் ரஷ்யாவின் அதிபராகத் தேர்ந்தெடுக்கப்பட்டார். இப்போது மாஸ்கோவில் இரண்டு அதிகார மையங்கள் இருந்தன: சோவியத் ஒன்றியத்தினது, ரஷ்யாவினது."),
  ("Gorbachev tried one more way to hold the country together. In a referendum in March nineteen ninety-one, about three out of four voters said yes to a renewed union, though six republics refused to take part. He began negotiating a new Union Treaty that would give the republics far more power.",
   f"நாட்டை ஒன்றாக வைத்திருக்க கோர்பச்சேவ் இன்னொரு வழியை முயன்றார். {Y[1991]} மார்ச்சில் நடந்த வாக்கெடுப்பில், ஏறத்தாழ நான்கில் மூன்று பங்கு வாக்காளர்கள் புதுப்பிக்கப்பட்ட ஒன்றியத்துக்கு ஆம் என்றனர்; ஆறு குடியரசுகள் அதில் பங்கேற்க மறுத்தன. குடியரசுகளுக்கு மிக அதிக அதிகாரம் தரும் புதிய ஒன்றிய ஒப்பந்தம் குறித்து அவர் பேச்சுவார்த்தை தொடங்கினார்."),
 ]),
 dict(id="C9", en="The Coup", ta="சதிப்புரட்சி", years=(1991, 1991), segs=[
  ("The new treaty was due to be signed on the twentieth of August nineteen ninety-one. Hardliners in the government, the army and the KGB feared that it would end the Soviet Union as they knew it. They decided to act first.",
   f"அந்தப் புதிய ஒப்பந்தம் {Y[1991]} ஆகஸ்ட் இருபதாம் தேதி கையெழுத்தாக இருந்தது. அரசாங்கம், இராணுவம், கே.ஜி.பி ஆகியவற்றில் இருந்த கடும்போக்காளர்கள், அது தாங்கள் அறிந்த சோவியத் ஒன்றியத்தை முடித்துவிடும் என்று அஞ்சினர். அவர்கள் முந்திக்கொண்டு செயல்பட முடிவு செய்தனர்."),
  ("On the morning of the nineteenth, Soviet radio announced that Gorbachev was ill, and that an emergency committee had taken power. In fact, he was being held under guard at his holiday home in Crimea. Tanks rolled into Moscow.",
   "பத்தொன்பதாம் தேதி காலை, கோர்பச்சேவ் உடல்நலமில்லாமல் இருப்பதாகவும், ஓர் அவசரக் குழு அதிகாரத்தைக் கைப்பற்றியிருப்பதாகவும் சோவியத் வானொலி அறிவித்தது. உண்மையில், அவர் கிரிமியாவில் உள்ள தன் விடுமுறை இல்லத்தில் காவலில் வைக்கப்பட்டிருந்தார். மாஸ்கோவுக்குள் டாங்கிகள் நுழைந்தன."),
  ("But the plotters hesitated. They did not arrest Yeltsin. He went to the Russian parliament building, climbed onto a tank outside it, and called on people to resist. Thousands gathered to defend the building through the night. Three people died in clashes, but the army would not storm it.",
   "ஆனால் சதிகாரர்கள் தயங்கினர். அவர்கள் யெல்ட்சினைக் கைது செய்யவில்லை. அவர் ரஷ்ய நாடாளுமன்றக் கட்டடத்துக்குச் சென்று, அதன் வெளியே இருந்த ஒரு டாங்கியின் மேல் ஏறி, மக்களை எதிர்த்து நிற்க அழைத்தார். இரவு முழுவதும், ஆயிரக்கணக்கானோர் அந்தக் கட்டடத்தைப் பாதுகாக்கக் கூடினர். மோதல்களில் மூவர் இறந்தனர்; ஆனால் இராணுவம் அதைத் தாக்க மறுத்தது."),
  ("Within three days the coup collapsed. The plotters were arrested, and Gorbachev flew back to Moscow. But he returned to a different country. His authority was gone, and Yeltsin's had grown. Within days, Gorbachev resigned as head of the Communist Party, and its activities were suspended.",
   "மூன்றே நாட்களில் சதி தோற்றது. சதிகாரர்கள் கைது செய்யப்பட்டனர்; கோர்பச்சேவ் மாஸ்கோவுக்குத் திரும்பினார். ஆனால் அவர் திரும்பியது வேறொரு நாட்டுக்கு. அவரது அதிகாரம் போயிருந்தது; யெல்ட்சினுடையது வளர்ந்திருந்தது. சில நாட்களில் கோர்பச்சேவ் கம்யூனிஸ்ட் கட்சித் தலைவர் பதவியிலிருந்து விலகினார்; கட்சியின் செயல்பாடுகள் நிறுத்தப்பட்டன."),
 ]),
 dict(id="C10", en="The End", ta="முடிவு", years=(1991, 1991), segs=[
  ("The coup had finished off what it meant to save. One republic after another declared independence: Ukraine, Belarus, Moldova, Azerbaijan, Uzbekistan, and more. Moscow recognised the Baltic states in September. And in a referendum on the first of December, about nine out of ten Ukrainians voted for independence.",
   "எதைக் காப்பாற்ற நினைத்ததோ, அதையே அந்தச் சதி முடித்துவிட்டது. ஒன்றன்பின் ஒன்றாகக் குடியரசுகள் சுதந்திரம் அறிவித்தன: உக்ரைன், பெலாரஸ், மால்டோவா, அசர்பைஜான், உஸ்பெகிஸ்தான், இன்னும் பல. செப்டம்பரில் மாஸ்கோ பால்டிக் நாடுகளை அங்கீகரித்தது. டிசம்பர் முதல் தேதி நடந்த வாக்கெடுப்பில், பத்தில் ஒன்பது உக்ரைனியர்கள் சுதந்திரத்தை ஆதரித்தனர்."),
  ("Without Ukraine, a union made little sense. On the eighth of December nineteen ninety-one, the leaders of Russia, Ukraine and Belarus met at a hunting lodge in a forest in Belarus, and declared that the Soviet Union had ceased to exist. They created a looser Commonwealth of Independent States in its place.",
   f"உக்ரைன் இல்லாமல் ஒரு ஒன்றியத்துக்குப் பொருளில்லை. {Y[1991]} டிசம்பர் எட்டாம் தேதி, ரஷ்யா, உக்ரைன், பெலாரஸ் தலைவர்கள் பெலாரசின் ஒரு காட்டில் இருந்த வேட்டை மாளிகையில் சந்தித்து, சோவியத் ஒன்றியம் இனி இல்லை என்று அறிவித்தனர். அதன் இடத்தில், தளர்வான சுதந்திர நாடுகளின் பொதுநலவாயத்தை உருவாக்கினர்."),
  ("Two weeks later, in Alma-Ata, eleven republics agreed to join the Commonwealth. Gorbachev was still the president of the Soviet Union, but there was almost nothing left for him to govern.",
   "இரண்டு வாரங்கள் கழித்து, அல்மா-அட்டாவில், பதினொரு குடியரசுகள் அந்தப் பொதுநலவாயத்தில் சேர ஒப்புக்கொண்டன. கோர்பச்சேவ் இன்னும் சோவியத் ஒன்றியத்தின் அதிபராகவே இருந்தார்; ஆனால் ஆள்வதற்கு அவரிடம் கிட்டத்தட்ட எதுவும் மிச்சமில்லை."),
  ("On the twenty-fifth of December, Gorbachev went on television and announced his resignation. He said he had opposed the breakup of the country, but that events had gone beyond his control. He spoke of apprehension, and of hope.",
   "டிசம்பர் இருபத்தைந்தாம் தேதி, கோர்பச்சேவ் தொலைக்காட்சியில் தோன்றி, தன் பதவி விலகலை அறிவித்தார். நாடு பிளவுபடுவதை தான் எதிர்த்ததாகவும், ஆனால் நிகழ்வுகள் தன் கட்டுப்பாட்டை மீறிவிட்டதாகவும் சொன்னார். கவலையைப் பற்றியும் நம்பிக்கையைப் பற்றியும் பேசினார்."),
  ("That evening, the red flag of the Soviet Union was lowered over the Kremlin for the last time, and the white, blue and red flag of Russia rose in its place. The next day, the upper chamber of the Soviet parliament voted the Union out of existence. After sixty-nine years, it was over.",
   "அந்த மாலை, சோவியத் ஒன்றியத்தின் செங்கொடி கிரெம்ளின் மீது கடைசி முறையாக இறக்கப்பட்டது; அதன் இடத்தில் ரஷ்யாவின் வெள்ளை, நீலம், சிவப்புக் கொடி உயர்ந்தது. மறுநாள், சோவியத் நாடாளுமன்றத்தின் மேலவை, ஒன்றியம் இல்லாமல் போனதாக வாக்களித்தது. அறுபத்தொன்பது ஆண்டுகளுக்குப் பிறகு, எல்லாம் முடிந்தது."),
 ]),
 dict(id="C11", en="Why Did It Fall?", ta="ஏன் வீழ்ந்தது?", years=(1985, 1991), segs=[
  ("Why did it happen? Historians still argue. Some point to the economy: a system that could not keep up with the West, and could not afford the arms race. Others stress the damage done by Afghanistan and Chernobyl, which wore away trust in the state.",
   "ஏன் இப்படி நடந்தது? வரலாற்றாசிரியர்கள் இன்னும் விவாதிக்கின்றனர். சிலர் பொருளாதாரத்தைச் சுட்டிக்காட்டுகின்றனர்: மேற்குக்கு ஈடுகொடுக்க முடியாத, ஆயுதப் போட்டியைத் தாங்க முடியாத ஓர் அமைப்பு. மற்றவர்கள், ஆப்கானிஸ்தானும் செர்னோபிலும் அரசின்மீதான நம்பிக்கையைத் தேய்த்ததை வலியுறுத்துகின்றனர்."),
  ("Some emphasise nationalism, the pull of fifteen peoples, many of whom wanted to run their own affairs. Others point to the choices of individuals: Gorbachev's reforms, which weakened the old order before a new one was ready, and Yeltsin's drive for power. Few believe there was a single cause.",
   "சிலர் தேசியவாதத்தை வலியுறுத்துகின்றனர்: தங்கள் விவகாரங்களைத் தாங்களே நடத்த விரும்பிய பதினைந்து மக்களின் இழுவிசை. வேறு சிலர், தனிநபர்களின் முடிவுகளைச் சுட்டுகின்றனர்: புதிய ஒழுங்கு தயாராகும் முன்பே பழைய ஒழுங்கை வலுவிழக்கச் செய்த கோர்பச்சேவின் சீர்திருத்தங்கள்; யெல்ட்சினின் அதிகார வேட்கை. ஒரே காரணம் என்று எவரும் கருதுவதில்லை."),
  ("What nearly everyone agrees on is how quickly it came. Only a few years earlier, almost no one, in Moscow or in the West, had expected the Soviet Union to vanish in the lifetime of its last leader.",
   "கிட்டத்தட்ட அனைவரும் ஒப்புக்கொள்வது, அது எவ்வளவு வேகமாக வந்தது என்பதைத்தான். சில ஆண்டுகளுக்கு முன்பு வரை, மாஸ்கோவிலோ மேற்கிலோ, அதன் கடைசித் தலைவரின் வாழ்நாளிலேயே சோவியத் ஒன்றியம் மறையும் என்று கிட்டத்தட்ட யாரும் எதிர்பார்க்கவில்லை."),
 ]),
 dict(id="C12", en="Legacy", ta="விட்டுச்சென்றவை", years=(1991, 1991), segs=[
  ("Fifteen new countries emerged from the Union. Russia took the Soviet seat at the United Nations and inherited most of its armed forces. Ukraine, Belarus and Kazakhstan later agreed to give up the nuclear weapons on their soil.",
   "ஒன்றியத்திலிருந்து பதினைந்து புதிய நாடுகள் தோன்றின. ஐக்கிய நாடுகள் சபையில் சோவியத் இடத்தை ரஷ்யா பெற்றது; அதன் படைகளில் பெரும்பகுதியையும் பெற்றது. உக்ரைன், பெலாரஸ், கஜகஸ்தான் ஆகியவை தங்கள் மண்ணில் இருந்த அணு ஆயுதங்களை விட்டுக்கொடுக்கப் பின்னர் ஒப்புக்கொண்டன."),
  ("For millions of people, the nineteen-nineties brought hardship, inflation and uncertainty, along with new freedoms. The effects of that period, and of the Soviet Union's end, still shape the politics of Europe and Asia today.",
   "கோடிக்கணக்கான மக்களுக்கு, தொண்ணூறுகள் புதிய சுதந்திரங்களுடன், வறுமையையும் பணவீக்கத்தையும் நிச்சயமின்மையையும் கொண்டுவந்தன. அந்தக் காலகட்டத்தின் தாக்கங்களும், சோவியத் ஒன்றியத்தின் முடிவும், இன்றும் ஐரோப்பாவின், ஆசியாவின் அரசியலை வடிவமைக்கின்றன."),
  ("The flag came down in a single evening. But the questions it left behind, about power, freedom and the price of change, are still with us.",
   "கொடி ஒரே மாலையில் இறக்கப்பட்டது. ஆனால் அது விட்டுச்சென்ற கேள்விகள், அதிகாரம், சுதந்திரம், மாற்றத்தின் விலை பற்றியவை, இன்றும் நம்முடன் இருக்கின்றன."),
 ]),
]

import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import ta_override; ta_override.apply(CHAPTERS, Y)
except ImportError:
    pass

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    en, ta, idx = [], [], []
    for ch in CHAPTERS:
        for j, (e, t) in enumerate(ch["segs"], 1):
            en.append(e); ta.append(t); idx.append({"seg": len(en), "chapter": ch["id"], "local": j, "last_in_chapter": j == len(ch["segs"])})
    open(os.path.join(here, "en_full.txt"), "w", encoding="utf-8").write("\n\n".join(en) + "\n")
    open(os.path.join(here, "ta_full.txt"), "w", encoding="utf-8").write("\n\n".join(ta) + "\n")
    json.dump({"segments": idx, "chapters": [{k: v for k, v in c.items() if k != "segs"} | {"n": len(c["segs"])} for c in CHAPTERS]}, open(os.path.join(here, "chapters.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    import re
    wc = sum(len(x.split()) for x in en); tc = sum(len(re.sub(r"[\s.,;:?!\-–—'\"]", "", x)) for x in ta)
    print(f"segments: {len(en)}   EN words: {wc}   TA chars (no space/punct): {tc}")
    print("longest EN seg chars:", max(len(x) for x in en), "  longest TA seg chars:", max(len(x) for x in ta))
