class City:
    def __init__(self):
        self.grid = []
        self.errors = []
        self.coffee_shops = []
        self.coffee_shops_amount = 0
        self.distances_amount = 0
        self.case_num = 0
        self.case_started = False
        self.case_status = True

    def parse(self, name):
        file = open(name, 'r')
        line_num = 0
        coffee_shop_num = 0
        distance_num = 0

        for line in file:
            line_num += 1

            if self.case_started:
                coffee_shop_num += 1
                distance_num += 1

                if coffee_shop_num < self.coffee_shops_amount:
                    self.add_coffee_shop(line)
                elif distance_num < self.distances_amount and self.case_status:
                    self.get_optimal_position(distance_num)
                else:
                    self.print_result()
                    self.case_started = False
            else:
                self.start_case(line, line_num)

    def start_case(self, line, line_num):
        if len(line) == 4:
            try:
                length = int(line[0])
                width = int(line[1])
                self.coffee_shops_amount = int(line[2])
                self.distances_amount = int(line[3])
            except ValueError:
                self.errors.append('Error. All arguments must be Integers. Line %d' % line_num)

            self.fill_grid(length, width)
            self.case_started = True
            self.case_status = True

        else:
            self.errors.append('Error. City line must contain 4 arguments. Line %d' % line_num)

    def fill_grid(self, length, width):
        for x in range(0, length):
            locations = []
            for y in range(0, width):
                locations.append(0)
            self.grid.append(locations)

    def add_coffee_shop(self, line, line_num):
        dx = len(self.grid)
        dy = len(self.grid[0])

        if len(line) == 2:
            try:
                x = int(line[0])
                y = int(line[1])
            except ValueError:
                self.errors.append('Error. All arguments must be Integers. Line %d' % line_num)
                self.case_status = False

            if 1 < x < dx and 1 < y < dy:
                self.grid[x][y] = -1
                self.coffee_shops.append({'x': x, 'y': y})
            else:
                self.errors.append('Error. Wrong coffee shop coordinates. Line %d' % line_num)
                self.case_status = False
        else:
            self.errors.append('Error. Coffee shop line must contain 2 arguments. Line %d' % line_num)
            self.case_status = False

    def get_optimal_position(self, distance):
        self.mark_reachable_locations(distance)

        optimal_position = None
        max_reached = 0

        for i in range(0, distance + 1):
            for j in range(0, distance + 1):
                if self.grid[i][j] > max_reached:
                    max_reached = self.grid[i][j]
                    optimal_position = {'x': i, 'y': j}
                elif self.grid[i][j] == max_reached != 0:
                    if i < optimal_position['x'] and j <= optimal_position['y']:
                        optimal_position = {'x': i, 'y': j}

    def mark_reachable_locations(self, distance):
        for coffee_shop in self.coffee_shops:
            x = coffee_shop['x']
            y = coffee_shop['y']

            for i in range(-distance, distance + 1):
                for j in range(abs(i) - distance, distance - abs(i)):
                    try:
                        if self.grid[x + i][y + j] != -1:
                            self.grid[x + i][y + j] += 1
                    except IndexError:
                        pass

    def print_result(self):
        pass





