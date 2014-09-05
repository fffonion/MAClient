MAClient Plugin Document
================

*  [Overview](#overview)
*  [Hook Plugin](#hook-plugin)
  *  [Examples](#examples)
  *  [Structure](#structure)
  *  [Event Name](#event-name)
  *  [Demo](#demo)
*  [extra_cmd plugin](#extra_cmd-plugin)
  *  [Examples](#examples-1)
  *  [Structure](#structure-1)
  *  [Usable variables](#usable-variables)
  *  [Demo](#demo-1)

##Overview

MAClient has plugin support since version 1.50. plugin system is enabled when `enable_plugins` is set to 1. You can also enable/disable single plugin using the `disabled` config; to disable multiple plugins, use `|` to seperate their names.

Plugins are some Python scripts or native extensions under the plugins folder. All plugins are dynamically imported when maclient_plugin initialize. Plugins with name starts with `_` or under sub folders are NOT going to be imported. When having the same name, plugins have the priority following pyd>py>pyc=pyo.

There're two types of plugins. One appends actions before and after specified events(AKA [hook plugin](#hook-plugin)); the other one adds extra commands to the CLI ui(AKA [extra_cmd plugin](#extra_cmd-plugin)). __The two types exist inside single file.__

##Hook Plugin

###Examples

[example_hook](plugins/_example_hook.py) [bgm](plugins/bgm.py)

###Structure

Let's start with example_hook plugin as an example. In this example, we set up three hooks: before attacking fairy, after attacking fairy, before exploring; when these events occur, we print some stuff on the screen.


You should always import `plugin_prototype` super class from _prototype module. At the first of your plugin(we call it metadata), name your plugin, your name, the version. Any meta besides `__plugin_name__` is only optional:

```Python
from _prototype import plugin_prototype
__plugin_name__ = 'sample plugin'
__author = 'fffonion'
__version__ = 0.1
require_version = 1.71 #require MAClient version no less then given version number
require_feature_nologin = True #commands that can be excuted before a player logined (used in extra_cmd plugin)
```

Set up event hook. It's `ENTER`/`EXIT`+`_`+`EVENT_NAME`:
```Python
hooks = {'ENTER__fairy_battle':1,'EXIT__fairy_battle':1,'ENTER_explore':1}
```

###Event Name

* tasker task scheduler
* auto_check check if card pack and friendship point is full
* check_strict_bc check if strict bc is triggered
* set_card
* red_tea use red potion
* green_tea use green potion
* _use_item use item(including potion) >=v1.68
* explore explore: select area
* _explore_floor explore: explore in a floor
* gacha
* select_card_sell
* fairy_battle_loop
* fairy_select
* _fairy_battle
* like greet
* friends friend menu
* reward_box get reward box
* point_setting
* factor_battle
* invoke_autoset auto set card deck
* _exit MAClient exit >= v1.67
> * ~~sleeper sleeping scheduler >=v1.68~~

The decimal after event name means the priority when hook is invoked. Bigger number means higher priority. When several plugins have a same priority, they are invoked in a random order.

In the example, all hooks are set to priority 1 (lowest).

*Make this empty if not using extra_cmd mode*
```Python
extra_cmd = {}
```

The plugin class
```Python
class plugin(plugin_prototype):
  def __init__(self):
    self.__name__=__plugin_name__

  def ENTER_explore(self,*args, kwargs):
    print 'explore!'
    print args
    return args,kwargs

  def EXIT__fairy_battle(self,*args, kwargs):
    print 'fairy_battle done!'

  def ENTER__fairy_battle(self,*args, kwargs):
    print 'fairy_battle!'
    return args,kwargs
```
Class name must be plugin and inherit from plugin_prototype super class.

For every hook, there must be a method with the name same with hooked event. `*args` and `kwargs` are arguments being tranfered to the event. Return `args` and `kwargs` in a before hook will modify the arguments really transfered to the hooked event.

You can use `self.tuple_assign` (inherited from super class) to modify items in a tuple.

*If there's no return statement of a return without value, then the arguments will not be modified.*

*plugin class will be instantiated so you can save some state infomation*

You can refer to __[maclient.py](maclient.py)__ for dig out each event has what arguments.

###Demo

[bgm](plugins/bgm.py)


##extra_cmd plugin

###Examples

[web_helper](plugins/web_helper.py) [query_tool](plugins/query_tool.py)

###Structure

metadata is same as that in hook plugin, the difference is now you should fill the `extra_cmd` dict

key means the command name, value is function name to be called
```Python
extra_cmd={'web':'start_webproxy','w':'start_webproxy'}
```

Use functional structure. Inner function is not necessary to be named as __do__.
```Python
def start_webproxy(plugin_vals):
  def do(*args):
    .....
  return do
```

`plugin_vals` are some class variables of maclient. In fact it's `self.__dict__`

###Usable variables

    plugin_vals['poster'] poster instance of `maclient_network`, can be used to communicate with server, returns decrypted data
    plugin_vals['player'] player instance
    ├─.cards card data
    │  └ .db card databse {1:['First - Lancelot','5','19'],……}
    │  └ .cards player's cards, elements are object_dict types
    │  └ .sid(xxx) find card by serial id
    │  └ .mid(xxx) find card by master id, returns a list
    ├─.item item data
    │  └ .name item database {'1':'AP Potion', ...}
    │  └ .count item count {'1':123, ...}
    ├─.ap / bc
    │  └ ['cur'] current value
    │  └ ['max'] max value
    ├─.friendship_point / gold
    plugin_vals['loc'] server name
    plugin_vals['cookie'] session cookie
    plugin_vals['logger'] the logger instance

All variables can be found in __[maclient.py](maclient.py)__ with `self.` as prefix

###Demo

[web_helper](plugins/web_helper.py)
