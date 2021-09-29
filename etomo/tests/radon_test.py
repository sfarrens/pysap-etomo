import unittest
import numpy as np

from etomo.operators import Radon2D, Radon3D


class MyTestCase(unittest.TestCase):
    """
    Computes <R.x,y> and <x,Rt.y> for random x and y for each operator and checks
    if the results are close enough.
    """
    def setUp(self) -> None:
        """
        Initialize test
        img_size: image size (square)
        nb_proj: number of projections
        n_channels: number of channels to be tested
        """
        self.img_size = 100
        self.nb_proj = 36
        self.n_channels = [1, 2]

    def test2D(self):
        """
        Tests adjoint operator of 2D operator
        """
        theta = np.arange(0., 180., 180./self.nb_proj)
        for n_c in self.n_channels:
            radon_op_cpu = Radon2D(angles=theta, img_size=self.img_size,
                                   n_channels=n_c, gpu=False)
            radon_op_gpu = Radon2D(angles=theta, img_size=self.img_size,
                                   n_channels=n_c, gpu=True)

            # Create fake variables
            if n_c == 1:
                fake_data = np.random.rand(self.img_size, self.img_size)
                fake_adjoint_data = np.random.rand(self.nb_proj, self.img_size)
            else:
                fake_data = np.random.rand(n_c, self.img_size, self.img_size)
                fake_adjoint_data = np.random.rand(n_c, self.nb_proj,
                                                   self.img_size)

            # Check if <R.x,y> == <x,Rt.y>
            for radon_op in [radon_op_cpu, radon_op_gpu]:
                Rxy = np.sum(radon_op.op(fake_data) * fake_adjoint_data)
                xRty = np.sum(fake_data * radon_op.adj_op(fake_adjoint_data))
                print(Rxy,xRty)
                self.assertTrue(np.allclose(Rxy, xRty, rtol=1e-4))

    def test3D(self):
        """
        Tests adjoint operator of 2D operator
        """
        theta = np.arange(0., 180., 180./self.nb_proj)
        for n_c in self.n_channels:
            radon_op = Radon3D(angles=theta, img_size=self.img_size,
                               n_channels=n_c)

            # Create fake variables
            if n_c == 1:
                fake_data = np.random.rand(self.img_size, self.img_size,
                                           self.img_size)
                fake_adjoint_data = np.random.rand(self.img_size, self.nb_proj,
                                                   self.img_size)
            else:
                fake_data = np.random.rand(n_c, self.img_size, self.img_size,
                                           self.img_size)
                fake_adjoint_data = np.random.rand(n_c, self.img_size,
                                                   self.nb_proj, self.img_size)

            # Check if <R.x,y> == <x,Rt.y>
            Rxy = np.sum(radon_op.op(fake_data) * fake_adjoint_data)
            xRty = np.sum(fake_data * radon_op.adj_op(fake_adjoint_data))
            self.assertTrue(np.allclose(Rxy, xRty, rtol=1e-3))


if __name__ == '__main__':
    unittest.main()