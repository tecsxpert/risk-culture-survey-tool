package tool.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.web.servlet.MockMvc;

import org.testcontainers.containers.GenericContainer;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@Testcontainers
@ActiveProfiles("test")
class FullIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    /*
     -------------------------
     PostgreSQL Container
     -------------------------
     */
    @Container
    static PostgreSQLContainer<?> postgres =
            new PostgreSQLContainer<>("postgres:15-alpine")
                    .withDatabaseName("testdb")
                    .withUsername("postgres")
                    .withPassword("postgres");

    /*
     -------------------------
     Redis Container
     -------------------------
     */
    @Container
    static GenericContainer<?> redis =
            new GenericContainer<>("redis:7-alpine")
                    .withExposedPorts(6379);

    /*
     -------------------------
     Inject Container Config
     -------------------------
     */
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {

        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
        registry.add("spring.datasource.driver-class-name",
                () -> "org.postgresql.Driver");

        registry.add("spring.redis.host", redis::getHost);
        registry.add("spring.redis.port",
                () -> redis.getMappedPort(6379));

        registry.add("spring.jpa.hibernate.ddl-auto",
                () -> "update");
    }

    /*
     -------------------------
     FULL CRUD FLOW TEST
     -------------------------
     */
    @Test
    @WithMockUser(username = "admin", roles = {"ADMIN"})
    void fullCrudFlowTest() throws Exception {

        // ---------- CREATE ----------
        String response = mockMvc.perform(post("/surveys")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "title":"Risk Survey",
                                  "description":"Integration Test"
                                }
                                """))
                .andExpect(status().isCreated())
                .andReturn()
                .getResponse()
                .getContentAsString();

        Long surveyId =
                objectMapper.readTree(response)
                        .get("id")
                        .asLong();

        // ---------- READ ----------
        mockMvc.perform(get("/surveys"))
                .andExpect(status().isOk());

        // ---------- UPDATE ----------
        mockMvc.perform(put("/surveys/" + surveyId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "title":"Updated Survey"
                                }
                                """))
                .andExpect(status().isOk());

        // ---------- DELETE ----------
        mockMvc.perform(delete("/surveys/" + surveyId))
                .andExpect(status().isNoContent());
    }
}