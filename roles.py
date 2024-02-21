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

class VillageAlignment:
  pass
class WolfAlignment:
  pass

class Seer:
  alignment = VillageAlignment
  rank = 99
  def __repr__(self):
    return "Seer"
  def __eq__(self,other):
    return other.rank == self.rank
  def __lt__(self,other):
    return other.rank < self.rank
  def __gt__(self,other):
    return other.rank > self.rank
  def __hash__(self):
    return hash("Seer")

class Wolf:
  def __init__(self,rank):
    self.rank = rank
  def __repr__(self):
    return "Wolf(%s)" % self.rank
  def __eq__(self,other):
    return other.rank == self.rank
  def __lt__(self,other):
    return other.rank < self.rank
  def __gt__(self,other):
    return other.rank > self.rank
  def __hash__(self):
    return hash("Wolf") ^ self.rank
  alignment = WolfAlignment

class Villager:
  alignment = VillageAlignment
  rank = 98
  def __repr__(self):
    return "Villager"
  def __eq__(self,other):
    return other.rank == self.rank
  def __lt__(self,other):
    return other.rank < self.rank
  def __gt__(self,other):
    return other.rank > self.rank
  def __hash__(self):
    return hash("Villager")



currwolfrank = 0
villagerinst = Villager()
def getNewRole(rolename):
  if rolename == "Villager":
    return villagerinst
  elif rolename == "Wolf":
    global currwolfrank
    currwolfrank += 1
    return Wolf(currwolfrank)
  else:
    return globals()[rolename]()
