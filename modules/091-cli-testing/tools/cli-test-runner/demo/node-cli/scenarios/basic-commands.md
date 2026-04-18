# Cowsay CLI — Snapshot Test

## Phase 1: Basic Commands

Verify cowsay is installed and accessible.

> `command -v cowsay`
```
/usr/local/bin/cowsay
```

Check that it runs with default cow.

> `cowsay "Hello from snapshot testing!"`
```
 ______________________________
< Hello from snapshot testing! >
 ------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

## Phase 2: Different Characters

Test with a different character (tux the penguin).

> `cowsay -f tux "I am Tux"`
```
 __________
< I am Tux >
 ----------
   \
    \
        .--.
       |o_o |
       |:_/ |
      //   \ \
     (|     | )
    /'\_   _/'\
    \___)=(___/
```

Test thinking mode.

> `cowthink "Hmm, let me think about this..."`
```
 _________________________________
( Hmm, let me think about this... )
 ---------------------------------
        o   ^__^
         o  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

## Phase 3: List Available Characters

List all available cow files.

> `cowsay -l`
```
C3PO  R2-D2  USA  ackbar  aperture-blank  aperture  armadillo  atat  atom  awesome-face  banana  bearface  beavis.zen  bees  bill-the-cat  biohazard  bishop  black-mesa  bong  box  broken-heart  bud-frogs  bunny  cake-with-candles  cake  cat  cat2  catfence  charizardvice  charlie  cheese  chessmen  chito  claw-arm  clippy  companion-cube  cower  cowfee  cthulhu-mini  cube  daemon  dalek-shooting  dalek  default  docker-whale  doge  dolphin  dragon-and-cow  dragon  ebi_furai  elephant-in-snake  elephant  elephant2  explosion  eyes  fat-banana  fat-cow  fence  fire  flaming-sheep  fox  ghost  ghostbusters  glados  goat  goat2  golden-eagle  hand  happy-whale  hedgehog  hellokitty  hippie  hiya  hiyoko  homer  hypno  ibm  iwashi  jellyfish  karl_marx  kilroy  king  kiss  kitten  kitty  knight  koala  kosh  lamb  lamb2  lightbulb  lobster  lollerskates  luke-koala  mailchimp  maze-runner  mech-and-cow  meow  milk  minotaur  mona-lisa  moofasa  mooghidjirah  moojira  moose  mule  mutilated  nyan  octopus  okazu  owl  pawn  periodic-table  personality-sphere  pinball-machine  psychiatrichelp  psychiatrichelp2  pterodactyl  queen  radio  ren  renge  robot  robotfindskitten  roflcopter  rook  sachiko  satanic  seahorse-big  seahorse  sheep  shikato  shrug  skeleton  small  smiling-octopus  snoopy  snoopyhouse  snoopysleep  spidercow  squid  squirrel  stegosaurus  stimpy  sudowoodo  supermilker  surgery  tableflip  taxi  telebears  template  threader  threecubes  toaster  tortoise  turkey  turtle  tux-big  tux  tweety-bird  vader-koala  vader  weeping-angel  whale  wizard  wood  world  www  yasuna_01  yasuna_02  yasuna_03  yasuna_03a  yasuna_04  yasuna_05  yasuna_06  yasuna_07  yasuna_08  yasuna_09  yasuna_10  yasuna_11  yasuna_12  yasuna_13  yasuna_14  yasuna_16  yasuna_17  yasuna_18  yasuna_19  yasuna_20  ymd_udon  zen-noh-milk
```
