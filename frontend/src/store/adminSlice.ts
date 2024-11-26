import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AdminState {
  promptTemplates: string[];
  users: string[];
  knowledgeBase: string[];
}

const initialState: AdminState = {
  promptTemplates: [],
  users: [],
  knowledgeBase: [],
};

export const adminSlice = createSlice({
  name: 'admin',
  initialState,
  reducers: {
    addPromptTemplate: (state, action: PayloadAction<string>) => {
      state.promptTemplates.push(action.payload);
    },
    // Добавьте другие действия для управления состоянием администратора
  },
});

export const { addPromptTemplate } = adminSlice.actions;
export default adminSlice.reducer;