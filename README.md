# Игра Asteroids
Цель игры состоит в том, чтобы получить как можно больше очков, расстреливая астероиды и летающие тарелки и избегая при этом столкновения с обломками. Игрок управляет космическим кораблём в форме стрелки, которая может крутиться влево и вправо, а также двигаться и стрелять, но только вперёд. При движении импульс не сохраняется: если не включать двигатель, то корабль постепенно остановится. Игрок также может использовать гиперпространственный двигатель — это приводит к тому, что корабль исчезает и затем появляется в случайном месте экрана, с риском уничтожения из-за появления на месте астероида.

Каждый уровень начинается с появления нескольких астероидов, дрейфующих в случайных точках экрана. Края  завёрнуты друг к другу, например астероид, уходящий за верхний край экрана, появляется на нижнем и продолжает двигаться в том же направлении. Когда игрок попадает в астероид, он разбивается на обломки, которые меньше, но двигаются быстрее. Периодически появляется летающая тарелка; большая тарелка просто двигается от одного края экрана до другого, меньшие по размеру тарелки метят в игрока.
# ТЗ:
При входе в игру появляется главное меню, в котором пользователь может выбрать режим игры. Всего планируетя два режима:

<b>1.	Игра одному(с ботами). 
  Периодически, помимо астероидов, будут появляться космические корабли, которые будут атаковать игрока. Цель игры: Набрать максимальное количество очков до исчерапания всех жизней. Количество жизней будет зависеть от сложности, выбраной перед игрой. Соответственно чем выше сложность, тем меньше жизней будет предоставлено игроку. Очки будут начисляться за уничтожение астероидов, ботов или игроков. Количество получаемых очков также зависит и от объекта, который вы уничтожаете: уничтожив игрока, вы получите больше очков, чем за уничтожение астероида.</b>

<b> 2.	В игре вдвоем поле будет ограничено. В нём игроки, помимо астероидов, для победы должны уничтожить друг друга.</b>

Когда режим будет выбран, пользоватеь будет играть на поле.

В одиночной игре камера будет следить за игроком. Также планируется добавить различное оружие, изначально им будет являться пушка, стреляющая одиночными выстрелами. 
  
<b> Движение будет осуществляться следующим образом:</b>
  
<b> ⦁	При нажатии левых и правых кнопок будет лишь меняться угол наклона корабля, но  на напраление движения это не повлияет.</b>

<b> ⦁	При нажатии кнопки движения вперед, игроку будет передаваться ускорение по направлению корабля. Можно использовать сложение векторов.</b>

<b> ⦁	Если не нажимать на кнопку ускорения, со временем движение начнет замедляться. В конце концов корабль остановится. Для реализации можно вычислять разность вектора движения и вектора, противоположно направленного движению, но очень малого по модулю.</b>

<b> ⦁	также будет гипердвигатель, который будет перемещать игрока в случайную точку на карте.</b>

Астероиды изначально будут иметь случайную скорость и напрление движения. После попадания в них будут появляться более мелкие асиероиды, затем еще меньше и так далее.Могут появляться как большие астероиды, так и маленькие. 
