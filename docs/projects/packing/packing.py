import Rhino.Geometry as rh


class Room:

    def __init__(self, room, pt, r):

        self.name = room
        self.cp = pt
        self.radius = r
        self.neighbors = []

    # method for adding another instance to a list of neighbors
    def add_neighbor(self, other):
        self.neighbors.append(other)

    # method for checking distance to other room object and moving apart if they are overlapping
    def collide(self, other, alpha):

        d = self.cp.DistanceTo(other.cp)

        amount = 0

        if d < self.radius + other.radius:

            pt_2 = other.cp
            pt_1 = self.cp

            # get vector from self to other
            v = pt_2 - pt_1

            # change vector magnitude to 1
            v.Unitize()
            # set magnitude to half the overlap distance
            v *= (self.radius + other.radius - d) / 2
            # multiply by alpha parameter to control
            # amount of movement at each time step
            v *= alpha

            amount = v.Length

            # move other object
            t = rh.Transform.Translation(v)
            pt_2.Transform(t)

            # reverse vector and move self same amount
            # in opposite direction
            v.Reverse()
            t = rh.Transform.Translation(v)
            pt_1.Transform(t)

        return amount

    # method for checking distance to other instance and moving closer if they are not touching
    def cluster(self, other, alpha):

        d = self.cp.DistanceTo(other.cp)

        amount = 0

        if d > self.radius + other.radius:

            pt_2 = other.cp
            pt_1 = self.cp

            # get vector from self to other
            v = pt_2 - pt_1

            # change vector magnitude to 1
            v.Unitize()
            # set magnitude to half the overlap distance
            v *= (d - (self.radius + other.radius)) / 2
            # multiply by alpha parameter to control
            # amount of movement at each time step
            v *= alpha

            amount = v.Length

            # move self
            t = rh.Transform.Translation(v)
            pt_1.Transform(t)

            # reverse vector and move other object same amount
            # in opposite direction
            v.Reverse()
            t = rh.Transform.Translation(v)
            pt_2.Transform(t)

        return amount

    def get_circle(self):
        return rh.Circle(self.cp, self.radius)


def run(rooms, pts, radii, max_iters, alpha, adjacencies):
    print (rooms)
    print(adjacencies)

    room_list = []

    for i, pt in enumerate(pts):
        my_room = Room(rooms[i], pt, radii[i])
        room_list.append(my_room)

    # for each agent in the list, add the previous agent as its neighbor
    for i in range(len(room_list)):
        # agents[i].add_neighbor(agents[i-1])
        room_list[i].add_neighbor(adjacencies(i))

    for i in range(max_iters):

        total_amount = 0

        for j, room_1 in enumerate(room_list):

            # cluster to all agent's neighbors
            for room_2 in room_1.neighbors:
                total_amount += room_1.cluster(room_2, alpha)

            # collide with all agents after agent in list
            for room_2 in room_list[j+1:]:
                # add extra multiplier to decrease effect of cluster
                total_amount += room_1.collide(room_2, alpha/5)

        if total_amount < .01:
            break

    iters = i

    print("process ran for {} iterations".format(i))

    circles = []

    for my_room in room_list:
        circles.append(my_room.get_circle())

    return circles, iters
