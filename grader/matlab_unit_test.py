class PLTestCase:

    total_iters = 1

    @classmethod
    def get_total_points(self):

        tests = [y
                 for x, y in self.__dict__.items()
                 if x.startswith('test_')]
        
        if self.total_iters == 1:
            total = sum([t.__dict__["points"] for t in tests])
            
        else:
            once = sum(
                [
                    t.__dict__["points"]
                    for t in tests
                    if not t.__dict__.get("repeated", True)
                ]
            )
            several = sum(
                [
                    t.__dict__["points"]
                    for t in tests
                    if t.__dict__.get("repeated", True)
                ]
            )
            total = self.total_iters * several + once
        return total