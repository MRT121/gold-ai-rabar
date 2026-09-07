if prompt := st.chat_input("پرسیارەکەت لێرە بنووسە..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        # لۆژیکی وەڵامدانەوەی زیرەک و فێرخواز
        with st.chat_message("assistant"):
            response = ""
            if "سۆلانە" in prompt or "SOL" in prompt.upper():
                sol_p = all_intel['سۆلانە (SOL)']['Close'].iloc[-1]
                response = f"سۆلانە لە ئێستادا لە ئاستی ${sol_p:,.2f} دایە. بەهۆی خێرایی تۆڕەکەی و گەشەی NFT، من پێشبینی دەکەم لە مانگی داهاتوو ڕوو لە بەرزبوونەوە بکات ئەگەر بیتکۆین جێگیر بێت."
            elif "زێڕ" in prompt:
                gold_p = all_intel['زێڕ (XAU)']['Close'].iloc[-1]
                response = f"زێڕ هەمیشە وەک پەناگەی ئارام دەمێنێتەوە. ئێستا نرخ ${gold_p:,.2f} دۆلارە. بەپێی شیکاری من بۆ داتاکانی بانکی ناوەندی، زێڕ پێویستی بە دابەزینی دۆلار هەیە بۆ ئەوەی ئاستی نوێ بشکێنێت."
            elif "بیتکۆین" in prompt:
                btc_p = all_intel['بیتکۆین (BTC)']['Close'].iloc[-1]
                response = f"بیتکۆین وەک 'زێڕی دیجیتاڵی' کار دەکات. لە ئێستادا ئاستی ${btc_p:,.0f} دۆلار زۆر گرنگە. ئەگەر سەیری پێشبینی ٧ ڕۆژەی سەرەوە بکەیت، ئاراستەکەت بۆ ڕوون دەبێتەوە."
            else:
                response = "من بەردەوام لە جوڵەی نەوت و دراوە دیجیتاڵییەکان فێر دەبم. پێم بڵێ کام دراوە لای تۆ گرنگە تا شیکاری وردی بۆ بکەم؟"
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

except Exception as e:
    st.error(f"هەڵەیەک ڕوویدا لە بارکردنی داتا پڕۆفیشناڵەکان: {e}")
