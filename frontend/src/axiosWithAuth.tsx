import axios from 'axios';

const axiosWithAuth = (token: string) => {
  return axios.create({
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
};

export default axiosWithAuth;