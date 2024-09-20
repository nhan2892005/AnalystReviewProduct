import React, { useState } from 'react';
import { AppBar, Typography, Toolbar } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';

import tikilogo from '../../images/tikilogo.png';
import useStyles from './styles';
import { SearchBarContainer, SearchInput, SearchButton } from './styles';
import SearchIcon from '@mui/icons-material/Search';
import { getProductsBySearch } from '../../actions';

const Navbar = () => {
  const classes = useStyles();
  const [search, setSearch] = useState('');
  const [focused, setFocused] = useState(false);

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (search.trim()) {
      const formattedSearch = search.trim().replace(/\s+/g, '+');

      dispatch(getProductsBySearch( formattedSearch ));
      
      navigate(`/search?searchQuery=${formattedSearch || 'none'}`);
    } else {
      navigate('/');
    }
  };
  return (
    <AppBar className={classes.appBar} position="static" color="inherit">
      <div className={classes.brandContainer}>
        <Typography component={Link} to="/" className={classes.heading} variant="h2" align="center">
          Tiki's Assistant
        </Typography>
        <img className={classes.image} src={tikilogo} alt="icon" height="60" />
      </div>

      <Toolbar className={classes.toolbar}>
        <form onSubmit={handleSubmit}>
          <SearchBarContainer focused={focused}>
            <SearchInput
              placeholder="Tìm những gì bạn muốn"
              onFocus={() => setFocused(true)}
              onBlur={() => setFocused(false)}
              inputProps={{ 'aria-label': 'search' }}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <SearchButton type="submit" aria-label="search">
              <SearchIcon />
            </SearchButton>
          </SearchBarContainer>
        </form>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;