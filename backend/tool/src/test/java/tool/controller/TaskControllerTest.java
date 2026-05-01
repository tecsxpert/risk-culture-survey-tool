package tool.controller;

import tool.entity.Task;
import tool.security.JwtAuthenticationFilter;
import tool.security.JwtUtil;
import tool.service.TaskService;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.domain.*;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(TaskController.class)
@AutoConfigureMockMvc(addFilters = false)   // 🔥 IMPORTANT FIX
public class TaskControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private TaskService taskService;

    @MockBean
    private JwtUtil jwtUtil;   // 🔥 FIX missing bean

    @MockBean
    private JwtAuthenticationFilter jwtAuthenticationFilter; // 🔥 FIX filter crash

    @Test
    void testGetAllTasks() throws Exception {

        Page<Task> page = new PageImpl<>(List.of());

        Mockito.when(taskService.getAllTasks(0, 10, "id", "asc"))
                .thenReturn(page);

        mockMvc.perform(get("/tasks"))
                .andExpect(status().isOk());
    }

    @Test
    void testExportCSV() throws Exception {

        mockMvc.perform(get("/tasks/export"))
                .andExpect(status().isOk());
    }
}