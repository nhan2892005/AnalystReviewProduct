import { styled } from '@mui/system';
import { deepPurple } from '@mui/material/colors';
import { InputBase, IconButton } from '@mui/material';

export default styled((theme) => ({
    appBar: {
        borderRadius: '20px',
        margin: '10px 0', 
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '10px 40px', 
        backgroundColor: '#fff', 
        boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)', 
        [theme.breakpoints.down('sm')]: {
          margin: '0',
          padding: '10px 20px',
        },
        [theme.breakpoints.down('xs')]: {
          margin: '0',
          padding: '10px 15px', 
        },
      },
      heading: {
        color: 'rgba(0, 183, 255, 1)',
        textDecoration: 'none',
        transition: 'color 0.3s ease', 
        '&:hover': {
          color: 'rgba(0, 153, 204, 1)', 
        },
        [theme.breakpoints.down('xs')]: {
          fontSize: '1.5rem',
        },
      },
      image: {
        marginLeft: '20px', 
        borderRadius: '10px',
        boxShadow: '0 2px 6px rgba(0, 0, 0, 0.2)', 
        [theme.breakpoints.down('xs')]: {
          width: '40px', 
          height: '40px',
        },
      },
    toolbar: {
        display: 'flex',
        justifyContent: 'flex-end',
        width: '400px',
        [theme.breakpoints.down('sm')]: {
        width: '300px',
        display: 'contents',
        },
        [theme.breakpoints.down('xs')]: {
        width: '100px',
        display: 'block',
        },
    },
    profile: {
        display: 'flex',
        justifyContent: 'flex-start',
        width: '400px',
        [theme.breakpoints.down('sm')]: {
        width: '300px',
        display: 'contents',
        },
        [theme.breakpoints.down('xs')]: {
        width: '100px',
        display: 'ruby',
        },
    },
    userName: {
        display: 'flex',
        alignItems: 'center',
        [theme.breakpoints.down('xs')]: {
        display: 'none',
        },
        [theme.breakpoints.down('sm')]: {
        display: 'none',
        },
    },
    brandContainer: {
        display: 'flex',
        alignItems: 'center',
        [theme.breakpoints.down('xs')]: {
        flexDirection: 'column',
        width: '50%',
        alignSelf: 'start',
        },
    },
    purple: {
        color: theme.palette.getContrastText(deepPurple[500]),
        backgroundColor: deepPurple[500],
        margin: '0 30px',
        [theme.breakpoints.down('xs')]: {
        width: '30px',
        height: '30px',
        },
    },
    button: {
        [theme.breakpoints.down('sm')]: {
        width: '50%',
        alignSelf: 'center',
        },
        [theme.breakpoints.down('xs')]: {
        width: '80%',
        },
    },
    logout: {
        margin: '0 10px',
        [theme.breakpoints.down('sm')]: {
        width: '40%',
        },
        [theme.breakpoints.down('xs')]: {
        width: '40%',
        },
    },
    searchText: {
        width: '100%',
        [theme.breakpoints.down('sm')]: {
        width: '300px',
        },
        [theme.breakpoints.down('xs')]: {
        width: '100px',
        },
    },
}));

export const SearchBarContainer = styled('div')(({ theme, focused }) => ({
  display: 'flex',
  alignItems: 'center',
  borderRadius: '25px',
  backgroundColor: focused ? '#4A90E2' : '#B3E5FC',
  padding: '8px 16px',
  boxShadow: focused ? '0px 4px 12px rgba(0, 0, 0, 0.2)' : 'none',
  transition: 'background-color 0.3s ease, box-shadow 0.3s ease',
  width: '100%',
  maxWidth: '500px',
  margin: '0 auto',
}));

export const SearchInput = styled(InputBase)(({ theme }) => ({
  color: '#fff',
  marginLeft: theme.spacing(1),
  flex: 1,
  fontSize: '16px',
  '&::placeholder': {
    color: '#04171a',
    opacity: 0.7,
  },
}));

export const SearchButton = styled(IconButton)(({ theme }) => ({
    color: '#fff',
}));