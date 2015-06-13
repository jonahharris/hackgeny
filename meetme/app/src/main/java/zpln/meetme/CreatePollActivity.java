package zpln.meetme;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.EditText;

public class CreatePollActivity extends ActionBarActivity {

    static MiniPoll miniPoll;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Intent intent = getIntent();
        setContentView(R.layout.create_poll_view);


        LinearLayout mainView = (LinearLayout) findViewById(R.id.createPollView);
        final ScrollView scrollView = (ScrollView) mainView.getChildAt(0);
        final LinearLayout linearLayout = (LinearLayout) scrollView.getChildAt(0);
        Button addPollButton = (Button) findViewById(R.id.addPollButton);
        final CreatePollActivity that = this;

        addPollButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                miniPoll = new MiniPoll();
                miniPoll.name = ((EditText) linearLayout.getChildAt(0)).getText().toString();
                miniPoll.options = new String[6];
                for(int i = 0; i < 6; i++) {
                    String pollOption = ((EditText) linearLayout.getChildAt(i + 2)).getText().toString();
                    if (pollOption.length() == 0) {
                        miniPoll.options[i] = null;
                    } else {
                        miniPoll.options[i] = pollOption;
                    }
                }
                finish();
            }
        });
    }
}
