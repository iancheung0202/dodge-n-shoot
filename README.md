# Dodge n’ Shoot

**Introduction**

The game mainly is about two players facing a bunch of incoming missiles. When a player hits
a missile, one life will be deducted from him or her. As time goes on, the frequency of incoming
missiles spawning will gradually increase by 0. 05 % every second. When it reaches the
frequency of spawning 6 missiles per second, the frequency will no longer increase _(lag and
skill issues)_. The players’ target is to survive as long as they could with initially 3 lives, while
competing for a longer survival time. They can make use of rockets and different modifiers to
help them stay alive.

**Basic Controls**

Player 1 uses **WASD** keys to move the airplane and uses key **E** to fire a rocket

Player 2 uses **ARROW** keys to move the airplane and uses **SPACE** bar to fire a rocket

**Modifiers**

All modifiers will spawn together like the missiles in random positions and times. Some spawn
more frequently while some are relatively rare. Players obtain them by making contact with
them and collect them. The following is the list of all modifiers and their functions (in rarity
order):

**Cloud** : They spawn the most frequently (every second) and technically serves no purpose.
However, some missiles may hide under the clouds to make them undetectable, so watch out.

**Mega Supplement** : They spawn every **7 - 10 seconds**. Once obtained, the next rocket fired
by the player will have a 20% larger hitbox. Additionally, if the rocket hits an incoming missile,
the player will gain 1 additional life.

**Life Booster** : They spawn every **10 - 20 seconds**. Once obtained, the player will instantly
heal itself 1 life.

**Silver Bullet** : They spawn every **13 - 20 seconds**. Once obtained, the next rocket fired by
the player will pierce through all missiles.

**Shield Protector** : They spawn every **17 - 27 seconds**. Once obtained, the player will be
immune for the next 3 incoming missiles hit.


**Signs**

You will notice some texts hovering on your airplane when you fly. These indications can
clearly provide you the information of what your current defensive and offensive situation.

```
“ Normal ”: meaning the next rocket will be the normal ones (that does not pierce through)
```
```
“ Mega ”: meaning the next rocket will have a larger size and heal you when it hits (Mega Supplement)
```
```
“ Pierce ”: meaning the next rocket will pierce through incoming missiles (Silver Bullet)
```
```
The left green number indicates how many immunities left, in this example, 3 (Shield Protector)
```
When you are reloading, there will not be any signs: However, once you finish reloading,
the sign will reappear again, indicating the next whatever rocket is ready.

**Boss Fight**

There will be a huge ballistic missile with 44 lives spawning after any player survives until 444
seconds, and no more normal missiles will spawn afterwards It does not move horizontally, but
moves up and down vertically and follows the nearest player.

It also shoots rockets against players, and if the rocket shoot by the boss hits a player, that
player will have one life deducted. If a rocket initialized by the boss touches a rocket initialized
by a player, both rockets explode and disappear without dealing damage to anyone.

There are a total of 5 levels of boss: Easy, Normal, Hard, Master and Insane. The harder level,
the faster the boss chases you, the faster and the more rockets shoot. Note that during Boss
Fight, all modifiers will still spawn in a regular interval.

The target of the players is to defeat the ballistic missile together cooperatively by shooting
rockets, but at the same time, try to confuse the other player and play tricks on them to make
them die faster. If the player touches the ballistic missile, the player dies instantly. Once the
ballistic missile is defeated, that means you beat the game! Congratulations!

```
The red number indicates the lives of the ballistic missiles remaining
```

**Other Game Mechanics**

- In addition to an increase of frequency in spawning incoming missiles, the reload speed
    of rockets will also decrease over time _(0. 025 % per second)._ When the game initially
    starts, the reload speed is 5 seconds.
- All kinds of rockets take time reload at first. Obtaining modifiers like Mega Supplement
    and Silver Bullet DOES NOT mean you will instantly have the ammo to shoot the
    rocket, as the game will still wait for the corresponding reload speed after your previous
    rocket is shot.
- Please bear in mind that Mega Supplement and Silver Bullet CANNOT be used
    together. Obtaining another modifier will cancel the previous collected ability as the
    next rocket will accord the latest modifier when both Mega Supplement and Silver
    Bullet is obtained but has not been used. _For example, if you have collected Silver Bullet_
    _previously, but then obtained Mega Supplement afterwards, the next rocket fired will_
    _be Mega Supplement._ Other than these two, no more two modifiers will interfere each
    other.


