import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UserState {
  queryHistory: string[];
}

const initialState: UserState = {
  queryHistory: [],
};

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    addQuery: (state, action: PayloadAction<string>) => {
      state.queryHistory.push(action.payload);
    },
    // Добавьте другие действия для управления состоянием пользователя
  },
});

export const { addQuery } = userSlice.actions;
export default userSlice.reducer;