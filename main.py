# Copyright 2010 Vincent Verhoeven
#
# This file is part of bra-ket-wolf.
#
# bra-ket-wolf is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# bra-ket-wolf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with bra-ket-wolf.  If not, see <http://www.gnu.org/licenses/>.

import pickle
from cmd import Cmd
from math import floor

from multiverse import Multiverse

class Main(Cmd):
  def __init__(self):
    Cmd.__init__(self)
    self.prompt = "(Werewolf Setup) "
    self.players = []
    self.roles = []
    self.keep = 1.0
    self.game = None
  
  def update_roles(self):
    seer = 1
    wolf = floor(len(self.players) / 3)
    villager = len(self.players) - wolf - seer
    self.roles = [("Seer",seer),("Wolf",wolf),("Villager",villager)]
  
  def do_start(self,s):
    """[Setup] Start a new game! Requires the players and roles to be set."""
    if self.players == []:
      print (">> Unable to start. Please configure the player list.")
      return
    if self.roles == []:
      print (">> Unable to start. Please configure the roles list.")
      return
    self.game = Multiverse(self.players,self.roles,self.keep)
    print ("The game is starting now.\n")
    self.prompt = "(%s%s) " % self.game.time
  
  def do_players(self,s):
    """[Setup] Enter a comma-separated list of players. This will also reset
    the roles list to a sensible default."""
    if s == "":
      print (self.players)
    elif self.game is not None:
      print (">> The player list cannot be changed once the game has started.")
    else:
      #TODO: fix the string parsing
      players = s.split(",")
      self.players = players
      self.update_roles()
  
  def do_roles(self,s):
    """[Setup] Enter the roles to be used, in a format like
    roles Villager 3, Wolf 2, Seer 1"""
    if s == "":
      print (self.roles)
    elif self.game is not None:
      print (">> The roles list cannot be changed once the game has started.")
    else:
      roles = [role.strip().split(" ") for role in s.split(",")]
      roles = [(role,int(count)) for [role,count] in roles]
      self.roles = roles
  
  def do_keepfraction(self,s):
    """[Setup] Specify which fraction of the generated universes to keep. Defaults to 1.0."""
    if s == "":
      print (self.keep)
    elif self.game is not None:
      print (">> The game is in progress. This value can only be set during setup.")
    else:
      self.keep = float(s)
  
  def do_state(self,s):
    """[Night, Day] Returns the current state of the game."""
    if self.game is None:
      print (">> Hey, start the game first!")
    else:
      print (self.game)
  
  def do_table(self,s):
    """[Night, Day] Returns an overview table of the distribution of good and evil."""
    if self.game is None:
      print (">> Hey, start the game first!")
    else:
      print (self.game.getGoodEvilDeadTable(False))
  
  def do_namedtable(self,s):
    """[Night, Day] Returns an overview table of the distribution of good and evil, with player names."""
    if self.game is None:
      print (">> Hey, start the game first!")
    else:
      print (self.game.getGoodEvilDeadTable(True))
  
  def do_next(self,s):
    """[Night, Day] Advances to the next phase of the game."""
    if self.game is None:
      print (">> The game has not started. Did you mean 'start'?")
      return
    self.game.nextPhase()
    print ("It is now %s%s" % self.game.time)
    self.prompt = "(%s%s) " % self.game.time
  
  def do_kill(self,s):
    """[Day] kill <player>: kills a player, fixing their role."""
    if self.game is None:
      print (">> Hey, start the game first!")
      return
    if self.game.isNight():
      #TODO: add safety check
      print (">> WARNING: you are killing a player at night.")
    if s in self.players:
      self.game.killPlayer(s)
    else:
      print (">> Player {0:s} not found, did you mean 'attack {0:s}'?".format(s))
  
  def do_attack(self,s):
    """[Night] attack <player> <target>: wolf attack during night.
    Note: wolf attacks are only carried out by the dominant wolf in any given universe."""
    if self.game is None:
      print (">> Hey, start the game first!")
      return
    (player,target) = s.split(" ")
    if player in self.players and target in self.players:
      self.game.wolfAttack(player,target)
    else:
      print ("Error: player {0:s} or {1:s} not found!".format(player,target))
  
  def do_see(self,s):
    """[Night] see <player> <target>: seer vision during night.
    Note: these are executed immediately, so according to the rules
    you should input all the wolf attacks first."""
    if self.game is None:
      print (">> Hey, start the game first!")
      return
    (player,target) = s.split(" ")
    if player in self.players and target in self.players:
      result = self.game.seerAlignmentVision(player,target)
      print (result)
    else:
      print ("Error: player {0:s} or {1:s} not found!".format(player,target))
  
  def do_save(self,s):
    """[Night, Day] save [filename] : Saves the game, by default to 'current.bra-ket-wolf'.
    Optionally, specify a filename to save to."""
    if self.game is None:
        print (">> Hey, start the game first!")
        return
    filename = s
    if filename == "":
      filename = "current.bra-ket-wolf"
    #TODO: add safety check
    f = open(filename,"wb")
    pickle.dump(self.game,f)
    f.close()
  
  def do_load(self,s):
    """[Setup, Night, Day] load [filename] : Loads the game, by default from 'current.bra-ket-wolf' but you
    Optionally, specify a filename to load from.
    This uses pickle so standard security warning apply, do not open untrusted files."""
    filename = s
    if filename == "":
      filename = "current.bra-ket-wolf"
    f = open(filename,"rb")
    self.game = pickle.load(f)
    self.players = self.game.players
    self.roles = self.game.rolelist
    f.close()
  
  def do_exit(self,s):
    """[Setup, Night, Day] Exits the program."""
    #TODO: add safety check
    return True

if __name__ == "__main__":
  m = Main()
  m.cmdloop()
